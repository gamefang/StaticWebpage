import csv
import io

def analyze_csv():
    # 将 CSV 数据加载到内存
    csv_file = io.StringIO(csvData)
    reader = csv.DictReader(csv_file)

    # 查找匹配用户输入的行
    result = []
    for row in reader:
        if row["Name"] == userInput:
            result.append(f"Name: {row['Name']}, Age: {row['Age']}, Salary: {row['Salary']}")

    # 如果没有找到匹配项
    if not result:
        result.append("No matching records found.")

    # 返回多行文本
    return "\n".join(result)