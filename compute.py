import pandas as pd
import numpy as np
from collections import defaultdict

def min_transactions(transactions):
    
    balances = defaultdict(int)
    
    for debtor, creditor, amount in transactions:    
        balances[debtor] -= amount
        balances[creditor] += amount

    sorted_balances = sorted(balances.items(), key=lambda x: x[1])

    i, j = 0, len(sorted_balances) - 1
    transactions_list = []
    num_transactions = 0

    while i < j:
        
        debtor, debtor_balance = sorted_balances[i]
        creditor, creditor_balance = sorted_balances[j]

        if debtor_balance == 0:
            i += 1
        elif creditor_balance == 0:
            j -= 1
        else:
            min_transfer = min(-debtor_balance, creditor_balance)
            debtor_balance += min_transfer
            creditor_balance -= min_transfer
            transactions_list.append((debtor, creditor, min_transfer))
            num_transactions += 1


        # Increment i or decrement j only when the balances are settled
        if debtor_balance == 0:
            i += 1
        if creditor_balance == 0:
            j -= 1

    return num_transactions, transactions_list

def calculate(df):

    # Drop columns before Paid by
    df = df.iloc[:,3:]

    # Fill any NA with 0
    df = df.fillna(0)

    df['Total'] = df.iloc[:, 2:].sum(axis=1).astype(int)

    df['Per Head'] = df['Settlement Currency'] / df['Total']

    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df.dropna(inplace=True)

    df.insert(2, 'PerHead', df['Per Head'])

    df = df.drop(columns=['Per Head', 'Total'])

    df.iloc[:, 3:] = df.iloc[:, 3:].multiply(df['PerHead'], axis=0)

    df = df.drop(columns=['PerHead', 'Settlement Currency'])


    # Generate sets like Owes,To,Amount from the 2D Matrix of Paid by x Names 

    result_tuples = []

    for index, row in df.iterrows():
        name = row['Paid By']
        
        for col in df.columns[1:]:
            value = row[col]
            
            if value > 0:
                result_tuples.append((col, name, value))


    # Generate a new dataframe out of the sets array created above

    df = pd.DataFrame(result_tuples, columns=['Owes','To','Amount'])

    df_aggregated = df.groupby(['Owes', 'To'], as_index=False)['Amount'].sum()

    df.Amount = df.Amount.astype(int)

    transactions = [tuple(x) for x in df[['Owes', 'To', 'Amount']].values]

    num_transactions, transactions_list = min_transactions(transactions)

    result = pd.DataFrame(transactions_list, columns=['Owes','To','Amount'])

    condition = result['Amount'] < 0

    result.loc[condition, ['Owes', 'To']] = result.loc[condition, ['To', 'Owes']].values

    result.loc[condition, 'Amount'] = -1 * result.loc[condition, 'Amount'].values

    return result.to_html(classes='table-auto text-right', index=False, header=True, escape=False, col_space=100)








