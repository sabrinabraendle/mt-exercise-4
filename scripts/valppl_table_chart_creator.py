#! /bin/env/python

"""
To create the perplexity table and the line chart, cd into 'scripts' and run $ python3 valppl_table_chart_creator.py.
"""

import pandas as pd
from openpyxl.workbook import Workbook


def get_ppls(file):
    ppl_list = []

    with open(file, 'r', encoding='utf-8') as log:
        for line in log:
            # Each 500 steps, store the displayed step and validation perplexity
            if 'Validation result' in line:
                step = line.split(', ')[-4].split(':')[0].split(' ')[-1]
                ppl = line.split(', ')[-2].split(' ')[-1]
                ppl_list.append((step, ppl))

    return ppl_list


def create_table(ppls):
    df_list = []
    for step_tuple in ppls:
        step_row = int(step_tuple[0][0])
        base_row = float(step_tuple[0][1])
        pre_row = float(step_tuple[1][1])
        post_row = float(step_tuple[2][1])
        df_list.append((step_row, base_row, pre_row, post_row))
    ppl_df = pd.DataFrame(df_list, columns=['Validation ppl', 'Baseline', 'Prenorm', 'Postnorm'])
    ppl_df = ppl_df.set_index('Validation ppl')

    return ppl_df


def create_chart(ppl_table):
    ppl_plot = ppl_table.plot(figsize=(10,5))
    ppl_fig = ppl_plot.get_figure()

    ppl_fig.savefig('ppl.pdf')


def main():
    # Define file paths
    base_path = '../logs/deen_transformer_regular/baseline.log'
    pre_path = '../logs/deen_transformer_regular/baseline.log'
    post_path = '../logs/deen_transformer_regular/baseline.log'

    # Get all the steps and validation perplexities for the generation of the table and the chart
    base_ppl = get_ppls(base_path)
    pre_ppl = get_ppls(pre_path)
    post_ppl = get_ppls(post_path)

    all_ppls = list(zip(base_ppl, pre_ppl, post_ppl))

    # Create the table
    ppl_df = create_table(all_ppls)
    print(ppl_df)

    # Write data frame to csv file
    ppl_df.to_csv(r'perplexity_table.csv', header=True, index_label='Validation ppl')

    # Write data frame to excel file
    writer = pd.ExcelWriter('perplexity_table.xlsx', engine='openpyxl')
    ppl_df.to_excel(writer, header=True, index_label='Validation ppl', sheet_name='Val ppl')
    writer.save()
    writer.close()

    # Create and save the line charts
    create_chart(ppl_df)


if __name__ == '__main__':
    main()