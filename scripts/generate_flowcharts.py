import os
import ast
from pyflowchart import Flowchart

def normalize_indentation(code):
    """Нормализует отступы, чтобы избежать ошибок с unexpected indent."""
    lines = code.splitlines()
    if not lines:
        return ""

    # Найти минимальный отступ среди всех строк (игнорируя пустые строки)
    min_indent = float('inf')
    for line in lines:
        stripped = line.strip()
        if stripped:  # Игнорировать пустые строки
            min_indent = min(min_indent, len(line) - len(stripped))

    # Удалить минимальный отступ из всех строк
    normalized_lines = []
    for line in lines:
        if line.strip():  # Только для непустых строк
            normalized_lines.append(line[min_indent:])
        else:
            normalized_lines.append("")  # Сохранить пустые строки

    return "\n".join(normalized_lines)


def extract_flowchart_code(code, start_marker="# flowchart: start", end_marker="# flowchart: end"):
    """Извлекает код между управляющими метками."""
    lines = code.splitlines()
    in_flowchart_block = False
    extracted_lines = []

    for line in lines:
        if start_marker in line:
            in_flowchart_block = True
            continue
        elif end_marker in line:
            in_flowchart_block = False
            continue

        if in_flowchart_block:
            extracted_lines.append(line)

    extracted_code = "\n".join(extracted_lines)
    return normalize_indentation(extracted_code)

def get_methods_from_class(class_node):
    """Возвращает все методы класса."""
    methods = []
    for node in class_node.body:
        if isinstance(node, ast.FunctionDef):
            methods.append(node)
    return methods

def process_file(file_path):
    """Обрабатывает файл Python и создает блок-схемы для методов классов."""
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

        tree = ast.parse(code)

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                methods = get_methods_from_class(node)

                for method in methods:
                    method_name = method.name
                    method_code = ast.get_source_segment(code, method)

                    # Извлекаем только код между управляющими метками
                    filtered_code = extract_flowchart_code(method_code)

                    if filtered_code.strip():
                        try:
                            flowchart = Flowchart.from_code(filtered_code)
                            output_file = f"diagrams/{class_name}_{method_name}_flowchart.txt"

                            with open(output_file, 'w', encoding='utf-8') as out_file:
                                out_file.write(flowchart.flowchart())

                            print(f"Блок-схема для {class_name}.{method_name} сохранена в {output_file}")
                        except Exception as e:
                            print(f"Ошибка при обработке метода {class_name}.{method_name}: {e}")

def process_directory(directory):
    """Обходит все файлы в директории и обрабатывает их."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Обработка файла: {file_path}")
                process_file(file_path)

project_directory = "./immunity_agent"
process_directory(project_directory)
