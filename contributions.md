# Contributions

## Data Collection and Processing

### **Daren Yao (darenyao)**

- Collected and processed data related to **Culture, Music, and Sports of Pitsburgh and CMU** in Pittsburgh.
- Scraped **17 main pages** and **12+ related subpages**, totaling over **30+ pages**.
- Developed scripts for web scraping and data extraction.
- Designed test QA pairs based on the collected data.
- **txt files contributed by daren:**

``` txt
"PIT_Opera_Opera.txt"
"PIT_Opera_other.txt"
"PIT_Opera_TIMETOACT.txt"
"PIT_Opera_TOSCA.txt"
"PIT_Opera_WOMENEYE.txt"
"PIT_Riverhound_matches.txt"
"PITS_EXTRA_SPORT.txt"
"PSO_history_symp.txt"
"scape_manual.ipynb"
"schedule_pirates_1.txt"
"Sports.txt"
"AAD.txt"
"Byron_symp.txt"
"Carnegie_Museums_1.txt"
"Carnegie_Museums_2.txt"
"Carnegie_Museums_3.txt"
"Carnegie_Museums_history.txt"
"Carnegie_Museums_space_1.txt"
"Carnegie_Museums_space_2.txt"
"Carnegie_Museums_space_3.txt"
"Carnegie_Museums_space_4.txt"
"CEO_symp.txt"
"CM_FP.txt"
"CM_HHC_history.txt"
"CM_MR.txt"
"CM_TF_events.txt"
"CM_WPSM.txt"
"events_Pitt_Cultral_TRUST.txt"
"events_Symphony.txt"
"food_festivals.txt"
"HEINZ_HALL_history_symp.txt"
"Jacob_symp.txt"
"Moon_symp.txt"
"Music_Director_symp.txt"
"Musicians_symp.txt"
"Opera_myth.txt"
"PENGUINS_MATCH.txt"
"picklesburgh_wiki.txt"
"PIT_Opera_ARMIDA.txt"
"PIT_Opera_CAVA.txt"
"PIT_Opera_CURLEW.txt"
"PIT_Opera_DEA.txt"
"PIT_Opera_DH.txt"
"PIT_Opera_FALSTAFF.txt"
"PIT_Opera_FELLOW.txt"
"PIT_Opera_History.txt"
"PIT_Opera_LA.txt"
"PIT_Opera_M.txt"
"PIT_Opera_MADAMA.txt"
```

### **Ruike Chen (ruikec)**

- Collected and processed data related to **General information, History, and Events of Pittsburgh and CMU**.
- Scraped **13 main pages** and **10 related subpages**, totaling over **30+ pages**.
- Developed scripts for web scraping and data extraction.
- Designed test QA pairs based on the collected data.
- **txt files contributed by ruike:**  

``` txt

"cmu_rankings.txt"
"cmu_traditions.txt"
"cmu_Vision,mission,value.txt"
"downtownpittsburgh_events.txt"
"event_visitpittsburgh.txt"
"institution and service privilege tax.txt"
"local services tax.txt"
"non-resident sports facility tax.txt"
"paper_pittsburgh_events.txt"
"parking tax.txt"
"payroll tax.txt"
"pittsburgh_britannica.txt"
"pittsburgh_events.txt"
"pittsburgh_history_wiki.txt"
"pittsburgh_wiki.txt"
"2024 budget operation.txt"
"amusement tax.txt"
"cmu_about.txt"
"cmu_awards.txt"
"cmu_events.txt"
"cmu_events_page.txt"
"cmu_history.txt"
"cmu_leadership.txt"
```

### **Overall Data Volume**

- The total extracted text data amounted to **2.14 MB** in `.txt` format.

## Modeling Contributions

### **Jinsong Yuan (jinsongy)**

- Built a **RAG (Retrieval-Augmented Generation) model** with **BM25 as the retriever**, **MiniLM as the reranker**, and **Flan-T5-783M as the prompter**.
- Developed an automated pipeline using **LangChain** for seamless data processing and model integration.
- Performed **data chunking** to improve retrieval efficiency and applied **few-shot learning** to enhance prompt formatting.
- Evaluated model performance using **BLEU, ROUGE, and BERTScore**, observing **high BERTScore** but lower ROUGE due to structural variations in responses.
- Compared different reranking methods, testing **MiniLM vs. Cohere Rerank API**, optimizing performance while considering API limitations.
