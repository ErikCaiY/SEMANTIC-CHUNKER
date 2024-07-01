from semanticChunker.agentic_chunker import AgenticChunker_kimi
from langchain_community.document_loaders import PyPDFLoader
# from modelscope.pipelines import pipeline
# from modelscope.utils.constant import Tasks
# from modelscope.outputs import OutputKeys
import logging
import json
import os

with open('config.json') as config_file:
    config = json.load(config_file)

api_key = config['api_key']
source_dir = config['source_dir']
log_file = config['log_file']
save_path = config['save_path']
# document_segmentation_model = config['document_segmentation_model']
model_name = config['model_name']
temperature = config['temperature']
max_token = config['max_token']

if not os.path.exists(save_path):
    os.makedirs(save_path)

logging.basicConfig(
    level=logging.INFO,
    filename=log_file,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

ac = AgenticChunker_kimi(
    kimi_api_key=api_key, 
    model=model_name, 
    temperature=temperature, 
    max_token=max_token
    )

# 文档分段工具
# p = pipeline(
#         task=Tasks.document_segmentation,
#         model=document_segmentation_model,
#         )

def read_pdf(file_path: str) -> str:
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    contents = []
    for page in pages:
        contents.append(page.page_content)
    return ''.join(contents)
    
def get_split(file_path: str, save_path=save_path):
    test_pdf = read_pdf(file_path=file_path)
    # document = p(test_pdf)
    # print(document)
    # propositions = document[OutputKeys.TEXT].split('\n\t')[:-1]
    # propositions = propositions[:-1]
    # split_res = ac.segment_pdf(propositions)
    split_res = ac.segment_pdf(test_pdf)

    save_name = ''.join((os.path.basename(file_path)).split('.')[:-1])
    # print(split_res)
    with open(os.path.join(save_path, save_name+'.txt'), 'w', encoding='utf-8') as f:
        f.write(split_res)

def get_pdf_files(directory):
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files


if __name__=="__main__":
    pdf_list = get_pdf_files(source_dir)
    logging.info(f'There has {len(pdf_list)} pdf files waiting for processing.\n{pdf_list}')
    for i, pdf_file in enumerate(pdf_list, start=1):
        logging.info(f'processing {pdf_file}.')
        try:
            get_split(pdf_file)
        except Exception as e:
            logging.warning(f'processing {pdf_file} failed. No.{i}.\n{e}')




