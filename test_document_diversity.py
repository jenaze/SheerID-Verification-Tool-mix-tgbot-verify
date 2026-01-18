"""
测试文档生成多样性

运行此脚本生成多张测试图片,检查:
- 大学/学区是否多样化
- 文档类型是否多样化
- 视觉效果是否有变化
"""

import sys
import os

# 确保 utils 可导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_student_documents():
    """测试学生文档生成（Spotify/YouTube/One模块）"""
    from spotify import img_generator as student_gen
    from utils.document_templates import DocumentType
    
    print("=" * 60)
    print("测试学生认证文档生成")
    print("=" * 60)
    
    # 生成10张不同的文档
    for i in range(10):
        try:
            first_name = f"Student{i+1}"
            last_name = "Test"
            
            # 让系统自动选择文档类型和大学
            img_data = student_gen.generate_image(first_name, last_name)
            
            filename = f"test_output/student_sample_{i+1}.png"
            os.makedirs("test_output", exist_ok=True)
            
            with open(filename, 'wb') as f:
                f.write(img_data)
            
            print(f"✓ 样本 {i+1}: 生成成功 ({len(img_data)} bytes) -> {filename}")
            
        except Exception as e:
            print(f"✗ 样本 {i+1}: 失败 - {e}")
    
    print()


def test_teacher_documents():
    """测试教师文档生成（K12/Boltnew模块）"""
    from k12 import img_generator as teacher_gen
    from utils.document_templates import DocumentType
    
    print("=" * 60)
    print("测试教师认证文档生成")
    print("=" * 60)
    
    # 生成10张不同的文档
    for i in range(10):
        try:
            first_name = f"Teacher{i+1}"
            last_name = "Test"
            
            # 让系统自动选择文档类型和学区
            img_data = teacher_gen.generate_teacher_png(first_name, last_name)
            
            filename = f"test_output/teacher_sample_{i+1}.png"
            os.makedirs("test_output", exist_ok=True)
            
            with open(filename, 'wb') as f:
                f.write(img_data)
            
            print(f"✓ 样本 {i+1}: 生成成功 ({len(img_data)} bytes) -> {filename}")
            
        except Exception as e:
            print(f"✗ 样本 {i+1}: 失败 - {e}")
    
    print()


def test_specific_document_types():
    """测试特定文档类型"""
    from spotify import img_generator as student_gen
    from k12 import img_generator as teacher_gen
    from utils.document_templates import DocumentType
    
    print("=" * 60)
    print("测试特定文档类型生成")
    print("=" * 60)
    
    # 测试学生文档类型
    student_doc_types = [
        DocumentType.CLASS_SCHEDULE,
        DocumentType.TUITION_RECEIPT,
        DocumentType.ENROLLMENT_VERIFICATION,
    ]
    
    for doc_type in student_doc_types:
        try:
            img_data = student_gen.generate_image("John", "Doe", doc_type=doc_type)
            filename = f"test_output/student_{doc_type.value}.png"
            
            with open(filename, 'wb') as f:
                f.write(img_data)
            
            print(f"✓ 学生 {doc_type.value}: 生成成功 -> {filename}")
            
        except Exception as e:
            print(f"✗ 学生 {doc_type.value}: 失败 - {e}")
    
    # 测试教师文档类型
    teacher_doc_types = [
        DocumentType.EMPLOYMENT_VERIFICATION,
        DocumentType.PAYROLL_STUB,
    ]
    
    for doc_type in teacher_doc_types:
        try:
            img_data = teacher_gen.generate_teacher_png("Jane", "Smith", doc_type=doc_type)
            filename = f"test_output/teacher_{doc_type.value}.png"
            
            with open(filename, 'wb') as f:
                f.write(img_data)
            
            print(f"✓ 教师 {doc_type.value}: 生成成功 -> {filename}")
            
        except Exception as e:
            print(f"✗ 教师 {doc_type.value}: 失败 - {e}")
    
    print()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("tgbot-verify 文档生成多样性测试")
    print("=" * 60 + "\n")
    
    # 运行所有测试
    test_student_documents()
    test_teacher_documents()
    test_specific_document_types()
    
    print("=" * 60)
    print("测试完成!")
    print("=" * 60)
    print("\n请检查 test_output/ 目录中的生成文件,验证:")
    print("  1. 不同大学/学区的文档是否有明显差异")
    print("  2. 不同文档类型是否正确渲染")
    print("  3. 视觉效果是否自然真实\n")
