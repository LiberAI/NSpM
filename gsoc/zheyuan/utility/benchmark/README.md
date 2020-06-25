# Pipeline of Benchmark #
This benchmark pipeline uses irbench as a local tool to calculate metrics on final answers.

## To run the code
Firstly, you need to follow the instructions of NSpM to train the NMT model. Let's say that the model is trained on `monument_300`.

Then, run our pipeline to generate the answers JSON file
```bash
python benchmark.py --model <trained modle ID> --test <test set ID> [--answer <answers file name>]
```
For example:
```bash
python benchmark.py --model monument_300 --test qald-9-train-multilingual.qald.json
```

Finally, evaluate out answers using the irbench
Remember to clone the project of irebench and download their release jar file
```bash
java -jar irbench-v0.0.1-beta.2.jar -evaluate "qald-9-train-multilingual" "<yourpath>/answer.json" "f-score"
```
For other configurations details, please visit their [site](https://github.com/AKSW/irbench) and some tips are given for the jdk version in my [blogs](https://baiblanc.github.io/2020/06/23/GSOC-Week-Three/)