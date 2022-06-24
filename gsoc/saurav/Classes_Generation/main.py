import os
import argparse
from subordinate import categorize_subordinate, refine_subordinate
from con_disjunction import categorize_con_disjunction, refine_con_disjunction
from comparative import categorize_comparative, refine_comparative
from superlative import categorize_superlative, refine_superlative
from numeric import categorize_numeric, refine_numeric
from utils import read, write_data, make_dir

def categorize_templates(data, output_dir):
    
    # Subordinate
    subordinate_data = categorize_subordinate(data)
    make_dir(output_dir+'/subordinate')
    write_data(output_dir+'/subordinate/templates', subordinate_data)

    # Con/disjunction
    con_disjunction_data = categorize_con_disjunction(data)
    make_dir(output_dir+'/con_disjunction')
    write_data(output_dir+'/con_disjunction/templates', con_disjunction_data)

    # Comparative
    comparative_data = categorize_comparative(data)
    make_dir(output_dir+'/comparative')
    write_data(output_dir+'/comparative/templates', comparative_data)

    # Superlative
    superlative_data = categorize_superlative(data)
    make_dir(output_dir+'/superlative')
    write_data(output_dir+'/superlative/templates', superlative_data)

    # Numeric
    numeric_data = categorize_numeric(data)
    make_dir(output_dir+'/numeric')
    write_data(output_dir+'/numeric/templates', numeric_data)

def refine_templates(output_dir):
    
    # Subordinate 
    subordinate_data = refine_subordinate(output_dir)
    write_data(output_dir+'/subordinate/refined_templates', subordinate_data)

    # Con/disjunctions
    con_disjunction_data = refine_con_disjunction(output_dir)
    write_data(output_dir+'/con_disjunction/refined_templates', con_disjunction_data)

    # Comparative
    comparative_data = refine_comparative(output_dir)
    write_data(output_dir+'/comparative/refined_templates', comparative_data)

    # Superlative
    superlative_data = refine_superlative(output_dir)
    write_data(output_dir+'/superlative/refined_templates', superlative_data)

    # Numeric
    numeric_data = refine_numeric(output_dir)
    write_data(output_dir+'/numeric/refined_templates', numeric_data)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--final_template_generator', dest='final_template_generator', 
                                metavar='final_template_generator', help='final template generator file', required=True)
    requiredNamed.add_argument('--output_dir', dest='output_dir', 
                                metavar='output_dir', help='output dir', required=True)
    args = parser.parse_args()
    final_template_generator = args.final_template_generator
    output_dir = args.output_dir

    data = read(final_template_generator)
    categorize_templates(data, output_dir)
    refine_templates(output_dir)
