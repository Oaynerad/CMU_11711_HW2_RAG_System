import json
import re

def classify_question(question):
    q_lower = question.lower().strip()

    # 1. time: 常见触发词(when, what year, what time, date等)
    if re.search(r'\bwhen\b', q_lower) or "what year" in q_lower or "what time" in q_lower:
        return "time"
    
    # 2. location: 常见触发词(where, which city, which place, 在哪里, 位置等)
    if re.search(r'\bwhere\b', q_lower) or "which city" in q_lower or "location" in q_lower:
        return "location"
    
    # 3. person: 关键词(who, which person, which famous person)
    if re.search(r'\bwho\b', q_lower) or "which person" in q_lower or "which famous" in q_lower:
        return "person"
    
    # # 4. reason: 通常带"why"或者"原因" only one QA
    # if re.search(r'\bwhy\b', q_lower):
    #     return "reason"
    
    # 5. quantity: "how many", "how much"
    if re.search(r'how many\b', q_lower) or re.search(r'how much\b', q_lower):
        return "quantity"
    
    # 6. how: 如果出现“How”，但又不属于“How many/much” # only 10 QAs
    if re.search(r'\bhow\b', q_lower):
        return "how"
    
    # 7. definition: “What is …”, “What was …”, “What are …”
    if q_lower.startswith("what "):
        return "definition"
    if q_lower.startswith("what's "):  # 如果有简写
        return "definition"

    # 如果都没匹配上，就丢到一个“fallback”或“other”类里
    return "other"

def main():
    # 读入你的 JSON 文件
    input_filename = "QA/total_QA_test_data.json"
    with open(input_filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 用字典收集分类后的数据
    classified_data = {
        "time": [],
        "location": [],
        "person": [],
        "quantity": [],
        "how": [],
        "definition": [],
        "other": []
    }

    # 遍历问题列表，按分类结果将其append到对应列表中
    for qa_pair in data:
        question = qa_pair["question"]
        answer = qa_pair["answer"]
        category = classify_question(question)
        classified_data[category].append({"question": question, "answer": answer})

    # 分别写入不同的JSON文件
    for category, qa_list in classified_data.items():
        output_filename = f"{category}_QA.json"
        with open(output_filename, "w", encoding="utf-8") as out_f:
            json.dump(qa_list, out_f, indent=4, ensure_ascii=False)
        print(f"分类 {category} 写入完成，数量：{len(qa_list)} 条")

if __name__ == "__main__":
    main()
