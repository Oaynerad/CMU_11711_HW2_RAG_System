from typing import List, Optional, Sequence
from langchain.docstore.document import Document
from langchain.retrievers import BM25Retriever
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import torch
from transformers import pipeline
import os
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_compressors.rankllm_rerank import RankLLMRerank
from typing import List
from langchain.docstore.document import Document
from langchain.retrievers import BM25Retriever
from langchain_community.document_compressors.rankllm_rerank import RankLLMRerank
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

from typing import List
from langchain.docstore.document import Document
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from langchain.retrievers import BM25Retriever
from langchain_community.llms import Cohere

from transformers import pipeline

from typing import List
from langchain.docstore.document import Document
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
import getpass
import os
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.llms import Cohere
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser
from sentence_transformers import CrossEncoder
from langchain_core.documents.compressor import BaseDocumentCompressor
from langchain_core.callbacks import Callbacks
from pydantic import Field

from pydantic import Field, PrivateAttr

class CrossEncoderReranker(BaseDocumentCompressor):
    #将top_k声明为Pydantic 字段
    top_k: int = Field(1, description="Number of top documents to return")
    #声明一个私有属性来存储CrossEncoder
    _reranker: CrossEncoder = PrivateAttr()

    def __init__(
        self,
        model_name_or_path: str = "cross-encoder/ms-marco-MiniLM-L-12-v2",
        top_k: int = 1,
        use_gpu: bool = True,
        **kwargs
    ):
        """Pydantic 要求在 super().__init__ 中显式传入已声明字段 (如 top_k)。"""
        super().__init__(top_k=top_k, **kwargs)

        device = "cuda" if use_gpu else "cpu"
        #将 CrossEncoder模型存储到私有属性里
        self._reranker = CrossEncoder(model_name_or_path, device=device)

    def rerank(self, query: str, docs: List[Document]) -> List[Document]:
        if not docs:
            return []
        pairs = [(query, d.page_content) for d in docs]
        scores = self._reranker.predict(pairs)
        docs_with_scores = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        top_docs = [d for d, s in docs_with_scores[: self.top_k]]
        return top_docs

    def compress_documents(
        self, documents: Sequence[Document], query: str, callbacks: Optional[Callbacks] = None
    ) -> Sequence[Document]:
        """Required by BaseDocumentCompressor; delegates to `rerank`."""
        return self.rerank(query, list(documents))
    
def build_langchain_pipeline(
    documents: List[Document],
    default_prompt_template: str,
    
    q_list: List[str],
    a_list: List[str], 
    topk: int = 1,
    use_gpu: bool = True,
    top_k: int = 1,
):
    #fewshotpipeline = FewShotPipeline(q_list, a_list, topk)
    bm25_retriever = BM25Retriever.from_documents(documents,k=100)#input: List[Document],run :query:str->List[Document]
    '''
    if "COHERE_API_KEY" not in os.environ:
        os.environ["COHERE_API_KEY"] = getpass.getpass("Cohere API Key:")
    compressor = CohereRerank(model="rerank-english-v3.0", top_n = 1)
    reranker = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=bm25_retriever)#input query:str->List[Document]
    '''
    reranker1 = CrossEncoderReranker(top_k = top_k)

    reranker = ContextualCompressionRetriever(
        base_compressor=reranker1, base_retriever=bm25_retriever
    )



    device = "cuda" if use_gpu else "cpu"
    # hf_gen_pipeline = pipeline(
    #     "text2text-generation",
    #     model="MBZUAI/LaMini-Flan-T5-783M",
    #     torch_dtype="auto",
    #     max_length=2048,
    #     device=device,
    # )
    from huggingface_hub import login

    login(token="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")
    hf_gen_pipeline = pipeline(
    "text-generation",
    model="mistralai/Mistral-7B-Instruct-v0.3",
    torch_dtype="auto",
    device=device,
    )
    # hf_gen_pipeline = pipeline(
    # "text-generation",
    # model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    # torch_dtype="auto",
    # device=device,
    # max_new_tokens=20,
    # do_sample=False,
    # temperature=1e-6,
    # )

    
    llm = HuggingFacePipeline(pipeline=hf_gen_pipeline)

    prompt_temp = PromptTemplate(
        template=default_prompt_template,
        input_variables=["context", "question", "few_shot_example"],
    )
    chain = prompt_temp | llm | StrOutputParser()

    def run(query: str) -> str:
        reranked_docs = reranker.invoke(query)
        reranked_docs = [d.page_content for d in reranked_docs]
        
        top_docs = reranked_docs[:top_k]
        ##############################消融实验
        # top_docs = reranked_docs[:0]
        #print(top_docs)
        context = "\n\n".join(doc for doc in top_docs)
        #few_shot_example = fewshotpipeline.run(query)#进入query输出相关question的qa对
        #return chain.invoke({"context": context, "question": query, "few_shot_example": few_shot_example})
        return chain.invoke({"context": context, "question": query})

    return run
'''
class FewShotPipeline:
    def __init__(self, q_list, a_list, topk=1):
        self.documents = [Document(page_content=q, metadata={"answer": a}) for q, a in zip(q_list, a_list)]
        self.retriever = BM25Retriever.from_documents(self.documents, k=topk)
        self.topk = topk

    def run(self, query):
        retrieved_docs = self.retriever.get_relevant_documents(query)
        few_shot_samples = "\n\n".join(
            f"Q: {doc.page_content}\nA: {doc.metadata['answer']}" for doc in retrieved_docs
        )
        return few_shot_samples
'''
def load_txt_files(folder_path):
    docs = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            docs.append(Document(page_content=content, metadata={"source": file_path}))
                except Exception as e:
                    print(f"fail to load {file_path} error: {e}")

    return docs

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class ParagraphThenCharacterSplitter:
    def __init__(self, chunk_size=200, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def split_document(self, doc):
        paragraphs = doc.page_content.split("\n\n")
        final_chunks = []

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                small_chunks = self.splitter.split_text(paragraph)
                for chunk in small_chunks:
                    final_chunks.append(Document(page_content=chunk, metadata=doc.metadata))

        return final_chunks

    def process(self, docs):
        processed_docs = []
        for doc in docs:
            processed_docs.extend(self.split_document(doc))
        return processed_docs

def predict_answers(pipeline_fn, queries):
    answers = []
    for query in queries:
        answer = pipeline_fn(query)
        answer = extract_answer(answer)
        answers.append(answer)
    return answers

def load_qa_pairs(question_file_path, answer_file_path):
    with open(question_file_path, "r", encoding="utf-8") as file:
        questions = [line.strip() for line in file.readlines() if line.strip()]
    with open(answer_file_path, "r", encoding="utf-8") as file:
        answers = [line.strip() for line in file.readlines() if line.strip()]
    return questions, answers

def save_list_to_txt(sentences, file_path, encoding="utf-8"):
    try:
        with open(file_path, "w", encoding=encoding) as f:
            for sentence in sentences:
                f.write(sentence.strip() + "\n")
        print(f"successfully save the txt: {file_path}")
    except Exception as e:
        print(f"fail to save, error: {e}")

import sacrebleu
from rouge_score import rouge_scorer
from bert_score import score

# def evaluate(predictions, references):
#     bleu_score = sacrebleu.corpus_bleu(predictions, [references])
#     print(f"BLEU: {bleu_score.score:.2f}")
#     scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

#     rouge1, rouge2, rougel = 0.0, 0.0, 0.0
#     for pred, ref in zip(predictions, references):
#         scores = scorer.score(ref, pred)
#         rouge1 += scores['rouge1'].fmeasure
#         rouge2 += scores['rouge2'].fmeasure
#         rougel += scores['rougeL'].fmeasure

#     n = len(predictions)
#     rouge1_avg = rouge1 / n
#     rouge2_avg = rouge2 / n
#     rougel_avg = rougel / n

#     print(f"ROUGE-1(F): {rouge1_avg:.4f}")
#     print(f"ROUGE-2(F): {rouge2_avg:.4f}")
#     print(f"ROUGE-L(F): {rougel_avg:.4f}")

#     P, R, F1 = score(predictions, references, lang="en", verbose=True)

#     print(f"BERTScore P:  {P.mean():.4f}")
#     print(f"BERTScore R:  {R.mean():.4f}")
#     print(f"BERTScore F1: {F1.mean():.4f}")

import string
def normalize_text(text):
    text = text.lower()
    for p in string.punctuation:
        text = text.replace(p, " ")
    tokens = text.split()
    tokens = [w for w in tokens if w not in ["a", "an", "the"]]
    
    return tokens

def exact_match_score(prediction, ground_truth):
    pred_tokens = normalize_text(prediction)
    gt_tokens   = normalize_text(ground_truth)
    return 1 if pred_tokens == gt_tokens else 0

def f1_score(prediction, ground_truth):
    pred_tokens = normalize_text(prediction)
    gt_tokens   = normalize_text(ground_truth)
    common = 0
    gt_token_count   = {}
    pred_token_count = {}
    for t in gt_tokens:
        gt_token_count[t] = gt_token_count.get(t, 0) + 1
    for t in pred_tokens:
        pred_token_count[t] = pred_token_count.get(t, 0) + 1
    for t in pred_token_count:
        if t in gt_token_count:
            common += min(pred_token_count[t], gt_token_count[t])
    
    precision = 1.0 * common / len(pred_tokens)
    recall    = 1.0 * common / len(gt_tokens)
    
    if precision + recall == 0:
        return 0.0, recall
    return 2 * precision * recall / (precision + recall), recall

def evaluate(predictions, ground_truths):
    em_total = 0.0
    f1_total = 0.0
    recall_total = 0.0
    n = len(predictions)
    
    for pred, gt in zip(predictions, ground_truths):
        em_total += exact_match_score(pred, gt)
        f1, recall = f1_score(pred, gt)
        f1_total += f1
        recall_total += recall

        
    exact_match = 100.0 * em_total / n
    macro_f1 = 100.0 * f1_total / n
    macro_recall = 100.0 * recall_total / n
    
    print("exact_match:",exact_match, "macro_f1:",macro_f1, "macro_recall:",macro_recall)


import json

def list_to_json(data_list, file_path="output.json"):
    output_dict = {}

    for i, sentence in enumerate(data_list, start=1):
        key = str(i)
        if key in output_dict:
            output_dict[key] += "; " + sentence
        else:
            output_dict[key] = sentence
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(output_dict, f, ensure_ascii=False, indent=4)

    print(f"json saved: {file_path}")

def extract_answer(text):
    text = text.split("Answer:", 1)[-1].strip()
    return text.split("\n\n", 1)[0].strip()

if __name__ == "__main__":
    folder_path = r"D:\hw2_new\data"
    docs = load_txt_files(folder_path)
    docs_processed = ParagraphThenCharacterSplitter().process(docs)
    sample_docs = docs_processed
    # default_prompt = (
    #     "Given the following context:\n{context}\n\n"
    #     "Question: {question}\n"
    #     "Please answer as concisely, make the answer short."
    #     "you don't need to answer a full sentence, just answer the question. "
    #     "if question is when, answer specific time, if question is who, answer specific person, if question is what, answer specific thing. Like following examples"
    #     "question: Who created the terrible towel at 1975? Myron Cope"
    #     "rather than Myron Cope created the terrible towel at 1975"
    #     "question: When was the Banana Split, an iconic part of American dessert culture invented? 1904"
    #     "rather than 1904 was the Banana Split, an iconic part of American dessert culture invented"
    #     "question: What is Melia Tourangeau's role at Pittsburgh Symphony Orchestra ?President and CEO"
    #     "rather than President and CEO is Melia Tourangeau's role at Pittsburgh Symphony Orchestra"
        
        
    # )
    default_prompt = ('''Only output several words of answer, not a full sentence. Don't output examples and contexts.

    Example:
    Q: Who created the terrible towel in 1975?
    A: Myron Cope

    Context:
    {context}

    Question: {question}
    Answer:'''
    )

    questions, answers = load_qa_pairs(
        question_file_path=r"D:\hw2_new\test.txt",
        answer_file_path=r"C:\Users\25353\Downloads\CMU_11711_HW2_RAG_System-QA-QA_different_type\qa_val\person_QA_a.txt"
    )
    pipeline_fn = build_langchain_pipeline(
        documents=sample_docs,
        default_prompt_template=default_prompt,
        use_gpu=True,
        top_k=3,
        q_list=questions,
        a_list=answers
    )
    answer = pipeline_fn("When is the 'Marvel Infinity Saga' event scheduled?")
    answer = extract_answer(answer)
    print('____________',answer)
    

    predictions = predict_answers(pipeline_fn, questions)
    list_to_json(predictions, file_path="output.json")
    save_list_to_txt(predictions, "predictions.txt")
    # evaluate(predictions, answers)