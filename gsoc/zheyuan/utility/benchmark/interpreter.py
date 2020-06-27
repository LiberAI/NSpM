import os

def interprete(trained_model_folder):
    os.chdir('../../../../nmt')
    os.system('pwd')
    print('start')
    folder_name = 'data/'+trained_model_folder
    os.system(
        'python -m nmt.nmt  --vocab_prefix=../' + folder_name + '/vocab --model_dir=../' + folder_name + '_model  --inference_input_file=../gsoc/zheyuan/utility/benchmark/to_ask.txt  --inference_output_file=../gsoc/zheyuan/utility/benchmark/output.txt --out_dir=../' + folder_name + '_model --src=en --tgt=sparql | tail -n4')

    os.system('''if [ $? -eq 0 ]
            then
                echo ""
                echo "ANSWER IN SPARQL SEQUENCE:"
                ENCODED="$(cat ../gsoc/zheyuan/utility/benchmark/output.txt)"
                python ../interpreter.py "${ENCODED}" > ../gsoc/zheyuan/utility/benchmark/output_decoded.txt
                cat ../gsoc/zheyuan/utility/benchmark/output_decoded.txt
                echo ""
            fi''')
    print('end')

if __name__ == "__main__":
    """
    Section to test the Interpreter.
    """
    interprete('monument_300')
    pass