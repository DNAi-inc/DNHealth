# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
API Documentation Generator.

Generates comprehensive API documentation from docstrings and module structure.
All operations enforce a 5-minute timeout limit and include timestamp logging.
"""

import ast
import inspect
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from tests.test_timeout_utils import DEFAULT_TEST_TIMEOUT, get_current_time

logger = logging.getLogger(__name__)

# Default timeout for operations (5 minutes)
OPERATION_TIMEOUT = DEFAULT_TEST_TIMEOUT


class APIDocumentationGenerator:
    """
    Generate API documentation from Python modules.
    
    Extracts docstrings, function signatures, class definitions, and module
    information to create comprehensive API reference documentation.
    """
    
    def __init__(self, source_dir: str, output_dir: str):
        """
        Initialize the API documentation generator.
        
        Args:
            source_dir: Path to source code directory
            output_dir: Path to output documentation directory
        """
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.start_time = time.time()
        current_time = get_current_time()
        logger.info(f"[{current_time}] APIDocumentationGenerator initialized")
        logger.info(f"[{current_time}] Source directory: {self.source_dir}")
        logger.info(f"[{current_time}] Output directory: {self.output_dir}")
    
    def generate_all_documentation(self) -> Dict[str, Any]:
        """
        Generate complete API documentation for all modules.
        
        Returns:
            Dictionary containing generation results:
            - modules_documented: Number of modules documented
            - functions_documented: Number of functions documented
            - classes_documented: Number of classes documented
            - output_files: List of generated output files
            - elapsed_time: Time taken for generation
            - timestamp: Completion timestamp
        """
        start_time = time.time()
        current_time = get_current_time()
        logger.info(f"[{current_time}] Starting API documentation generation")
        
        modules_documented = 0
        functions_documented = 0
        classes_documented = 0
        output_files = []
        
        # Find all Python modules
        python_files = list(self.source_dir.rglob("*.py"))
        
        # Filter out test files and __pycache__
        python_files = [
            f for f in python_files
            if "__pycache__" not in str(f) and "test_" not in f.name
        ]
        
        # Group by package
        packages: Dict[str, List[Path]] = {}
        for py_file in python_files:
            if time.time() - start_time > OPERATION_TIMEOUT - 10:
                logger.warning(f"[{get_current_time()}] Timeout approaching, stopping documentation generation")
                break
            
            # Get package name
            rel_path = py_file.relative_to(self.source_dir)
            package_parts = rel_path.parts[:-1]  # Exclude filename
            package_name = ".".join(package_parts) if package_parts else "root"
            
            if package_name not in packages:
                packages[package_name] = []
            packages[package_name].append(py_file)
        
        # Generate documentation for each package
        for package_name, files in packages.items():
            if time.time() - start_time > OPERATION_TIMEOUT - 5:
                break
            
            package_doc = self._generate_package_documentation(package_name, files)
            if package_doc:
                output_file = self._write_package_documentation(package_name, package_doc)
                if output_file:
                    output_files.append(output_file)
                    modules_documented += len(files)
                    functions_documented += package_doc.get("functions_count", 0)
                    classes_documented += package_doc.get("classes_count", 0)
        
        # Generate index
        index_file = self._generate_index(packages.keys(), output_files)
        if index_file:
            output_files.append(index_file)
        
        elapsed = time.time() - start_time
        end_time = get_current_time()
        
        result = {
            "modules_documented": modules_documented,
            "functions_documented": functions_documented,
            "classes_documented": classes_documented,
            "output_files": output_files,
            "elapsed_time": elapsed,
            "timestamp": end_time
        }
        
        logger.info(
            f"[{end_time}] API documentation generation completed: "
            f"{modules_documented} modules, {functions_documented} functions, "
            f"{classes_documented} classes, elapsed: {elapsed:.3f}s"
        )
        
        return result
    
    def _generate_package_documentation(        self, package_name: str, files: List[Path]
    ) -> Optional[Dict[str, Any]]:
        """
        Generate documentation for a package.
        
        Args:
            package_name: Name of the package
            files: List of Python files in the package
            
        Returns:
            Dictionary containing package documentation
        """
        package_doc = {
            "package_name": package_name,
            "modules": [],
            "functions_count": 0,
            "classes_count": 0
        }
        
        for py_file in files:
            try:
                module_doc = self._parse_module(py_file)
                if module_doc:
                    package_doc["modules"].append(module_doc)
                    package_doc["functions_count"] += len(module_doc.get("functions", []))
                    package_doc["classes_count"] += len(module_doc.get("classes", []))
            except Exception as e:
                logger.warning(f"[{get_current_time()}] Error parsing {py_file}: {str(e)}")
                continue
        
        return package_doc if package_doc["modules"] else None
    
    def _parse_module(self, py_file: Path) -> Optional[Dict[str, Any]]:
        """
        Parse a Python module and extract documentation.
        
        Args:
            py_file: Path to Python file
            
        Returns:
            Dictionary containing module documentation
        """
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(py_file))
            
            module_doc = {
                "name": py_file.stem,
                "path": str(py_file.relative_to(self.source_dir)),
                "docstring": ast.get_docstring(tree) or "",
                "functions": [],
                "classes": [],
                "constants": []
            }
            
            # Extract functions, classes, and constants
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_doc = self._extract_function_doc(node)
                    if func_doc:
                        module_doc["functions"].append(func_doc)
                elif isinstance(node, ast.ClassDef):
                    class_doc = self._extract_class_doc(node)
                    if class_doc:
                        module_doc["classes"].append(class_doc)
                elif isinstance(node, ast.Assign):
                    # Check if it's a constant (all caps)
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            const_doc = self._extract_constant_doc(node)
                            if const_doc:
                                module_doc["constants"].append(const_doc)
            
            return module_doc
            
        except Exception as e:
            logger.warning(f"[{get_current_time()}] Error parsing module {py_file}: {str(e)}")
            return None
    
    def _extract_function_doc(self, node: ast.FunctionDef) -> Optional[Dict[str, Any]]:
        """
        Extract documentation from a function node.
        
        Args:
            node: AST function node
            
        Returns:
            Dictionary containing function documentation
        """
        # Skip private functions (starting with _)
        if node.name.startswith("_"):
            return None
        
        func_doc = {
            "name": node.name,
            "docstring": ast.get_docstring(node) or "",
            "signature": self._format_signature(node),
            "args": []
        }
        
        # Extract arguments
        for arg in node.args.args:
            if arg.arg != "self":
                arg_info = {
                    "name": arg.arg,
                    "annotation": ast.unparse(arg.annotation) if arg.annotation else None
                }
                func_doc["args"].append(arg_info)
        
        return func_doc
    
    def _extract_class_doc(self, node: ast.ClassDef) -> Optional[Dict[str, Any]]:
        """
        Extract documentation from a class node.
        
        Args:
            node: AST class node
            
        Returns:
            Dictionary containing class documentation
        """
        # Skip private classes (starting with _)
        if node.name.startswith("_"):
            return None
        
        class_doc = {
            "name": node.name,
            "docstring": ast.get_docstring(node) or "",
            "bases": [ast.unparse(base) for base in node.bases],
            "methods": []
        }
        
        # Extract methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_doc = self._extract_function_doc(item)
                if method_doc:
                    class_doc["methods"].append(method_doc)
        
        return class_doc
    
    def _extract_constant_doc(self, node: ast.Assign) -> Optional[Dict[str, Any]]:
        """
        Extract documentation from a constant assignment.
        
        Args:
            node: AST assignment node
            
        Returns:
            Dictionary containing constant documentation
        """
        if not node.targets:
            return None
        
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            return None
        
        const_doc = {
            "name": target.id,
            "value": ast.unparse(node.value) if node.value else None
        }
        
        return const_doc
    
    def _format_signature(self, node: ast.FunctionDef) -> str:
        """
        Format function signature as string.
        
        Args:
            node: AST function node
            
        Returns:
            Formatted signature string
        """
        try:
            args = []
            for arg in node.args.args:
                arg_str = arg.arg
                if arg.annotation:
                    arg_str += f": {ast.unparse(arg.annotation)}"
                args.append(arg_str)
            
            signature = f"{node.name}({', '.join(args)})"
            
            if node.returns:
                signature += f" -> {ast.unparse(node.returns)}"
            

                    # Log completion timestamp at end of operation
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(f"Current Time at End of Operations: {current_time}")
            return signature
        except Exception:
            # Fallback if unparse fails
            return f"{node.name}(...)"
    
    def _write_package_documentation(
        self, package_name: str, package_doc: Dict[str, Any]
    ) -> Optional[str]:
        """
        Write package documentation to file.
        
        Args:
            package_name: Name of the package
            package_doc: Package documentation dictionary
            
        Returns:
            Path to generated file
        """
        try:
            # Create output file path
            safe_name = package_name.replace(".", "_") if package_name != "root" else "root"
            output_file = self.output_dir / f"{safe_name}_api.md"
            
            # Generate markdown content
            lines = [
                f"# {package_name} API Reference",
                "",
                f"**Generated:** {get_current_time()}",
                "",
                "## Overview",
                "",
                package_doc.get("overview", "Package documentation."),
                "",
                "## Modules",
                ""
            ]
            
            # Add module documentation
            for module in package_doc["modules"]:
                lines.extend([
                    f"### {module['name']}",
                    "",
                    f"**Path:** `{module['path']}`",
                    "",
                ])
                
                if module["docstring"]:
                    lines.extend([
                        "**Description:**",
                        "",
                        module["docstring"],
                        ""
                    ])
                
                # Add classes
                if module["classes"]:
                    lines.extend([
                        "#### Classes",
                        ""
                    ])
                    for cls in module["classes"]:
                        lines.extend([
                            f"##### {cls['name']}",
                            ""
                        ])
                        if cls["docstring"]:
                            lines.append(f"{cls['docstring']}")
                            lines.append("")
                        if cls["bases"]:
                            lines.append(f"**Bases:** {', '.join(cls['bases'])}")
                            lines.append("")
                        if cls["methods"]:
                            lines.append("**Methods:**")
                            lines.append("")
                            for method in cls["methods"]:
                                lines.append(f"- `{method['signature']}`")
                                if method["docstring"]:
                                    lines.append(f"  - {method['docstring'].split(chr(10))[0]}")
                            lines.append("")
                
                # Add functions
                if module["functions"]:
                    lines.extend([
                        "#### Functions",
                        ""
                    ])
                    for func in module["functions"]:
                        lines.extend([
                            f"##### {func['name']}",
                            "",
                            f"```python",
                            f"{func['signature']}",
                            f"```",
                            ""
                        ])
                        if func["docstring"]:
                            lines.append(func["docstring"])
                            lines.append("")
                        if func["args"]:
                            lines.append("**Parameters:**")
                            lines.append("")
                            for arg in func["args"]:
                                lines.append(f"- `{arg['name']}`" + 
                                           (f": {arg['annotation']}" if arg['annotation'] else ""))
                            lines.append("")
                
                lines.append("---")
                lines.append("")
            
            # Write to file
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            
            logger.info(f"[{get_current_time()}] Generated documentation: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"[{get_current_time()}] Error writing documentation: {str(e)}")
            return None
    
    def _generate_index(self, packages: Set[str], output_files: List[str]) -> Optional[str]:
        """
        Generate index file for all documentation.
        
        Args:
            packages: Set of package names
            output_files: List of generated output files
            
        Returns:
            Path to generated index file
        """
        try:
            index_file = self.output_dir / "API_INDEX.md"
            
            lines = [
                "# DNHealth API Documentation Index",
                "",
                f"**Generated:** {get_current_time()}",
                "",
                "## Packages",
                ""
            ]
            
            # Add package links
            for package in sorted(packages):
                safe_name = package.replace(".", "_") if package != "root" else "root"
                lines.append(f"- [{package}]({safe_name}_api.md)")
            
            lines.extend([
                "",
                "## Statistics",
                "",
                f"- **Total Packages:** {len(packages)}",
                f"- **Total Documentation Files:** {len(output_files)}",
                ""
            ])
            
            # Write index
            with open(index_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            
            logger.info(f"[{get_current_time()}] Generated index: {index_file}")
            return str(index_file)
            
        except Exception as e:
            logger.error(f"[{get_current_time()}] Error generating index: {str(e)}")
            return None


def generate_api_documentation(
    source_dir: Optional[str] = None,
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate complete API documentation for DNHealth.
    
    Args:
        source_dir: Path to source code directory (default: src/dnhealth)
        output_dir: Path to output documentation directory (default: docs/api)
        
    Returns:
        Dictionary containing generation results
    """
    start_time = time.time()
    current_time = get_current_time()
    logger.info(f"[{current_time}] Starting API documentation generation")
    
    # Set defaults
    if source_dir is None:
        source_dir = Path(__file__).parent.parent.parent / "src" / "dnhealth"
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / "docs" / "api"
    
    # Create generator
    generator = APIDocumentationGenerator(str(source_dir), str(output_dir))
    
    # Generate documentation
    result = generator.generate_all_documentation()
    
    elapsed = time.time() - start_time
    end_time = get_current_time()
    
    logger.info(
        f"[{end_time}] API documentation generation completed "
        f"(elapsed: {elapsed:.3f}s)"
    )
    
    return result
