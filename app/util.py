import aiohttp
import numpy as np


async def query_graph(uri: str, query: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(uri, json={'query': query}) as response:
            if 200 <= response.status <= 299:
                return await response.json()
            else:
                raise Exception(f"Failed HTTP Post request with status: {response.status}")


async def query_all_rep_holders(uri: str) -> list:
    result = []
    skip = 0
    query = '{{ \n \
      reputationHolders(first: 1000, skip:{skip}) {{ \n \
        address \n \
        balance \n \
        dao {{ \n \
          name \n \
        }} \n \
        createdAt \n \
      }} \n \
    }}'
    response = await query_graph(uri, query.format(skip=skip))
    while len(response['data']['reputationHolders']) > 0:
        result += response['data']['reputationHolders']
        skip += 1000
        response = await query_graph(uri, query.format(skip=skip))
    return result


def clean_rep_holders_data(df, dao_name):
    # filter by dao
    undict = lambda x: x['name']
    df['dao'] = df['dao'].apply(undict)
    df = df[df.dao == dao_name].reset_index(drop=True)

    # set data types
    df['address'] = df['address'].astype('string')
    df['balance'] = df['balance'].astype('string')
    df['createdAt'] = df['createdAt'].apply(int).astype('datetime64[s]')
    df['dao'] = df['dao'].astype('string')

    # handle uint64 overflow -> units now in quadrillions
    # first count and truncate final 15 (or fewer) digits
    units_fn = lambda x: min(len(x), 15)
    df['units'] = df['balance'].apply(units_fn)
    truncate = lambda x: x[0:len(x) - 15] if len(x) > 15 else len(x)
    df['balance_quadrillions'] = df['balance'].apply(truncate).astype('string').astype('float64')
    # log and recombine
    df['log10_balance'] = np.log10(df.balance_quadrillions) + df.units

    # sort and filter cols
    df.sort_values('balance_quadrillions', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df.loc[:, ['address', 'balance_quadrillions', 'log10_balance']]
