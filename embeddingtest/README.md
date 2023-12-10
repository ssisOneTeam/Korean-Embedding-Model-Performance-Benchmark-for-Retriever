# Embedding Testing

- Embedding Model은 [Chromadb](https://docs.trychroma.com)를 이용해 Model별 collection 지정 후 chroma 폴더에 저장 후 평가(질문 별 Hitrate)

### 임시 TODO
    Model 잡히면 Model 이름 저장해서 사용하기
    document에 들어갈 구조 다 잡히면 Model별 max_sequence에 따라서 split해서 Embedding하고 chroma에 넣기(persist directory 공개 예정)
    하고 나서 collection 수 1개 이상인 경우에만 사용할 수 있도록 하기(*testing/test_loader.ipynb 참조)

    Hitrate 평가