# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
Database integration utilities for DNHealth library.

Provides database storage and retrieval for HL7v2, HL7v3, and FHIR messages.
Supports SQLite by default with extensible architecture for other databases.
All database operations include timestamps in logs for traceability.
"""

import json
import sqlite3
import threading
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from dnhealth.errors import DNHealthError
from dnhealth.util.logging import get_logger

logger = logging.getLogger(__name__)

logger = get_logger(__name__)


class MessageType(Enum):
    """Message type enumeration."""

    HL7V2 = "hl7v2"
    HL7V3 = "hl7v3"
    FHIR = "fhir"


class DatabaseError(DNHealthError):
    """Base exception for database operations."""

    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when database connection fails."""

    pass


class DatabaseQueryError(DatabaseError):
    """Raised when database query fails."""

    pass


class MessageDatabase:
    """
    Database interface for storing and retrieving healthcare messages.

    Supports SQLite database with thread-safe operations.
    All operations include timestamps in logs for audit trail.

    Attributes:
        db_path: Path to SQLite database file
        connection: SQLite connection object
        lock: Thread lock for thread-safe operations
    """

    def __init__(self, db_path: Union[str, Path], auto_create: bool = True):
        """
        Initialize message database.

        Args:
            db_path: Path to SQLite database file
            auto_create: If True, create database file if it doesn't exist

        Raises:
            DatabaseConnectionError: If database connection fails
        """
        self.db_path = Path(db_path)
        self.auto_create = auto_create
        self.lock = threading.Lock()
        self._connection: Optional[sqlite3.Connection] = None

        # Ensure parent directory exists
        if self.auto_create:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database schema
        self._initialize_database()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{current_time}] Database initialized at {self.db_path}"
        )

    def _get_connection(self) -> sqlite3.Connection:
        """
        Get or create database connection.

        Returns:
            SQLite connection object

        Raises:
            DatabaseConnectionError: If connection fails
        """
        if self._connection is None:
            try:
                self._connection = sqlite3.connect(
                    str(self.db_path),
                    check_same_thread=False,
                    timeout=30.0,
                )
                # Enable row factory for dict-like access
                self._connection.row_factory = sqlite3.Row
                # Enable foreign keys
                self._connection.execute("PRAGMA foreign_keys = ON")
            except sqlite3.Error as e:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.error(
                    f"[{current_time}] Failed to connect to database: {e}"
                )
                raise DatabaseConnectionError(f"Database connection failed: {e}") from e

        return self._connection

    def _initialize_database(self) -> None:
        """Initialize database schema if it doesn't exist."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Create messages table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT UNIQUE NOT NULL,
                    message_type TEXT NOT NULL,
                    message_format TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Create indexes for faster queries
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_message_type
                ON messages(message_type)
            """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_message_id
                ON messages(message_id)
            """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_created_at
                ON messages(created_at)
            """
            )

            # Create message_tags table for flexible tagging
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS message_tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT NOT NULL,
                    tag_key TEXT NOT NULL,
                    tag_value TEXT,
                    FOREIGN KEY (message_id) REFERENCES messages(message_id)
                        ON DELETE CASCADE,
                    UNIQUE(message_id, tag_key)
                )
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tag_key_value
                ON message_tags(tag_key, tag_value)
            """
            )

            conn.commit()

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(
                f"[{current_time}] Database schema initialized successfully"
            )
        except sqlite3.Error as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(
                f"[{current_time}] Failed to initialize database schema: {e}"
            )
            raise DatabaseError(f"Schema initialization failed: {e}") from e

    def store_message(
        self,
        message_id: str,
        message_type: Union[MessageType, str],
        content: str,
        message_format: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None,
    ) -> int:
        """
        Store a message in the database.

        Args:
            message_id: Unique identifier for the message
            message_type: Type of message (HL7V2, HL7V3, FHIR)
            content: Message content (serialized)
            message_format: Format of the message (text, json, xml)
            metadata: Optional metadata dictionary
            tags: Optional tags dictionary for flexible querying

        Returns:
            Database row ID of the stored message

        Raises:
            DatabaseQueryError: If storage fails
        """
        with self.lock:
            try:
                conn = self._get_connection()
                cursor = conn.cursor()

                # Convert MessageType enum to string if needed
                if isinstance(message_type, MessageType):
                    message_type_str = message_type.value
                else:
                    message_type_str = str(message_type)

                # Serialize metadata to JSON
                metadata_json = json.dumps(metadata) if metadata else None

                # Insert message
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO messages
                    (message_id, message_type, message_format, content, metadata, updated_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                    (message_id, message_type_str, message_format, content, metadata_json),
                )

                # Store tags if provided
                if tags:
                    for tag_key, tag_value in tags.items():
                        cursor.execute(
                            """
                            INSERT OR REPLACE INTO message_tags
                            (message_id, tag_key, tag_value)
                            VALUES (?, ?, ?)
                        """,
                            (message_id, tag_key, str(tag_value)),
                        )

                conn.commit()
                row_id = cursor.lastrowid

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(
                    f"[{current_time}] Stored message {message_id} "
                    f"(type: {message_type_str}, format: {message_format})"
                )

                return row_id
            except sqlite3.Error as e:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.error(
                    f"[{current_time}] Failed to store message {message_id}: {e}"
                )
                raise DatabaseQueryError(f"Failed to store message: {e}") from e

    def get_message(        self, message_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a message by ID.

        Args:
            message_id: Unique identifier of the message

        Returns:
            Dictionary with message data or None if not found

        Raises:
            DatabaseQueryError: If query fails
        """
        with self.lock:
            try:
                conn = self._get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT * FROM messages WHERE message_id = ?
                """,
                    (message_id,),
                )

                row = cursor.fetchone()
                if row is None:
                    return None

                # Get tags for this message
                cursor.execute(
                    """
                    SELECT tag_key, tag_value FROM message_tags
                    WHERE message_id = ?
                """,
                    (message_id,),
                )
                tag_rows = cursor.fetchall()
                tags = {row["tag_key"]: row["tag_value"] for row in tag_rows}

                # Parse metadata JSON
                metadata = None
                if row["metadata"]:
                    try:
                        metadata = json.loads(row["metadata"])
                    except json.JSONDecodeError:
                        pass

                result = {
                    "id": row["id"],
                    "message_id": row["message_id"],
                    "message_type": row["message_type"],
                    "message_format": row["message_format"],
                    "content": row["content"],
                    "metadata": metadata,
                    "tags": tags,
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(
                    f"[{current_time}] Retrieved message {message_id}"
                )

                return result
            except sqlite3.Error as e:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.error(
                    f"[{current_time}] Failed to retrieve message {message_id}: {e}"
                )
                raise DatabaseQueryError(f"Failed to retrieve message: {e}") from e

    def query_messages(
        self,
        message_type: Optional[Union[MessageType, str]] = None,
        message_format: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        limit: Optional[int] = None,
        offset: int = 0,
        order_by: str = "created_at",
        order_desc: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Query messages with filters.

        Args:
            message_type: Filter by message type
            message_format: Filter by message format
            tags: Filter by tags (key-value pairs)
            limit: Maximum number of results
            offset: Offset for pagination
            order_by: Column to order by (default: created_at)
            order_desc: If True, order descending (default: True)

        Returns:
            List of message dictionaries matching the query

        Raises:
            DatabaseQueryError: If query fails
        """
        with self.lock:
            try:
                conn = self._get_connection()
                cursor = conn.cursor()

                # Build query
                conditions = []
                params = []

                if message_type:
                    if isinstance(message_type, MessageType):
                        message_type_str = message_type.value
                    else:
                        message_type_str = str(message_type)
                    conditions.append("m.message_type = ?")
                    params.append(message_type_str)

                if message_format:
                    conditions.append("m.message_format = ?")
                    params.append(message_format)

                # Handle tag filtering
                if tags:
                    for tag_key, tag_value in tags.items():
                        conditions.append(
                            """
                            EXISTS (
                                SELECT 1 FROM message_tags mt
                                WHERE mt.message_id = m.message_id
                                AND mt.tag_key = ? AND mt.tag_value = ?
                            )
                        """
                        )
                        params.extend([tag_key, tag_value])

                where_clause = ""
                if conditions:
                    where_clause = "WHERE " + " AND ".join(conditions)

                order_direction = "DESC" if order_desc else "ASC"
                order_clause = f"ORDER BY m.{order_by} {order_direction}"

                limit_clause = ""
                if limit:
                    limit_clause = f"LIMIT {limit} OFFSET {offset}"

                query = f"""
                    SELECT DISTINCT m.* FROM messages m
                    {where_clause}
                    {order_clause}
                    {limit_clause}
                """

                cursor.execute(query, params)
                rows = cursor.fetchall()

                # Get tags for each message
                results = []
                for row in rows:
                    cursor.execute(
                        """
                        SELECT tag_key, tag_value FROM message_tags
                        WHERE message_id = ?
                    """,
                        (row["message_id"],),
                    )
                    tag_rows = cursor.fetchall()
                    tags_dict = {
                        tag_row["tag_key"]: tag_row["tag_value"]
                        for tag_row in tag_rows
                    }

                    # Parse metadata JSON
                    metadata = None
                    if row["metadata"]:
                        try:
                            metadata = json.loads(row["metadata"])
                        except json.JSONDecodeError:
                            pass

                    results.append(
                        {
                            "id": row["id"],
                            "message_id": row["message_id"],
                            "message_type": row["message_type"],
                            "message_format": row["message_format"],
                            "content": row["content"],
                            "metadata": metadata,
                            "tags": tags_dict,
                            "created_at": row["created_at"],
                            "updated_at": row["updated_at"],
                        }
                    )

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(
                    f"[{current_time}] Query returned {len(results)} messages"
                )

                return results

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
            except sqlite3.Error as e:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.error(
                    f"[{current_time}] Failed to query messages: {e}"
                )
                raise DatabaseQueryError(f"Failed to query messages: {e}") from e

    def delete_message(self, message_id: str) -> bool:
        """
        Delete a message by ID.

        Args:
            message_id: Unique identifier of the message

        Returns:
            True if message was deleted, False if not found

        Raises:
            DatabaseQueryError: If deletion fails
        """
        with self.lock:
            try:
                conn = self._get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    DELETE FROM messages WHERE message_id = ?
                """,
                    (message_id,),
                )

                deleted = cursor.rowcount > 0
                conn.commit()

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if deleted:
                    logger.info(
                        f"[{current_time}] Deleted message {message_id}"
                    )
                else:
                    logger.warning(
                        f"[{current_time}] Message {message_id} not found for deletion"
                    )

                return deleted
            except sqlite3.Error as e:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.error(
                    f"[{current_time}] Failed to delete message {message_id}: {e}"
                )
                raise DatabaseQueryError(f"Failed to delete message: {e}") from e

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Dictionary with statistics (total messages, by type, etc.)

        Raises:
            DatabaseQueryError: If query fails
        """
        with self.lock:
            try:
                conn = self._get_connection()
                cursor = conn.cursor()

                # Total messages
                cursor.execute("SELECT COUNT(*) FROM messages")
                total_messages = cursor.fetchone()[0]

                # Messages by type
                cursor.execute(
                    """
                    SELECT message_type, COUNT(*) as count
                    FROM messages
                    GROUP BY message_type
                """
                )
                by_type = {
                    row["message_type"]: row["count"] for row in cursor.fetchall()
                }

                # Messages by format
                cursor.execute(
                    """
                    SELECT message_format, COUNT(*) as count
                    FROM messages
                    GROUP BY message_format
                """
                )
                by_format = {
                    row["message_format"]: row["count"]
                    for row in cursor.fetchall()
                }

                # Total tags
                cursor.execute("SELECT COUNT(DISTINCT message_id) FROM message_tags")
                tagged_messages = cursor.fetchone()[0]

                stats = {
                    "total_messages": total_messages,
                    "by_type": by_type,
                    "by_format": by_format,
                    "tagged_messages": tagged_messages,
                }

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(
                    f"[{current_time}] Retrieved database statistics: "
                    f"{total_messages} total messages"
                )

                return stats
            except sqlite3.Error as e:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.error(
                    f"[{current_time}] Failed to get statistics: {e}"
                )
                raise DatabaseQueryError(f"Failed to get statistics: {e}") from e

    def close(self) -> None:
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(
                f"[{current_time}] Database connection closed"
            )

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
