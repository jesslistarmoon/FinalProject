import sqlite3
from collections import defaultdict

DB_PATH = "./FinalProjectDB.db"

def calculate_borough_averages(output_txt="summary_results.txt"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    query = '''
        select
            b.id as borough_id,
            b.borough_name,
            c.id as collision_id,
            p.market_value as property_market_value
        from boroughs b
        join collisions c on b.id = c.borough_id
        join properties p on b.id = p.borough_id
        order by b.id;
    '''
    cur.execute(query)
    rows = cur.fetchall()

    query = '''
        select
            b.borough_name,
            bp.population
        from boroughs b
        join borough_population bp on b.id = bp.id;
    '''
    cur.execute(query)
    populations = cur.fetchall()

    query = '''
        select
            b.borough_name,
            count(p.id) as park_count
        from boroughs b
        left join parks p on b.id = p.borough_id
        group by b.id, b.borough_name
        order by b.borough_name;
    '''
    cur.execute(query)
    parks = cur.fetchall()
    conn.close()

    boroughcollisions = defaultdict(int)
    boroughpropertyvalue = defaultdict(list)
    boroughparks = defaultdict(int)
    boroughpopulation = defaultdict(int)

    for _, borough, collision_id, market_value in rows:
        boroughcollisions[borough]+=1
        boroughpropertyvalue[borough].append(market_value)

    for borough, population in populations:
        boroughpopulation[borough] = population

    for borough, count in parks:
        boroughparks[borough] = count

    results = {}
    for borough in boroughcollisions:
        results[borough] = {}
        results[borough]["marketvalue"] = sum(boroughpropertyvalue[borough])/len(boroughpropertyvalue[borough])
        results[borough]["collisionpercapita"] = boroughcollisions[borough]/boroughpopulation[borough]
        results[borough]["parkspercapita"] = boroughparks[borough]/boroughpopulation[borough]

    # Write to file
    with open(output_txt, "w") as f:
        f.write(f"{'Borough':<15} | {'Avg Market Value ($)':>22} | {'Collision per Capita (100000)':>28} | {'Parks per Capita (100000)':>27}\n")
        f.write(f"{'-' * 16}|{'-' * 24}|{'-' * 31}|{'-' * 28}\n")
        for borough, data in results.items():
            f.write(
                f"{borough:<15} | "
                f"${data['marketValue']:>21,.2f} | "
                f"{data['collisionPerCapita'] * 100000:>29.2f} | "
                f"{data['parksPerCapita'] * 100000:>27.2f}\n"
            )

    print(f"Results written to {output_txt}")

# Example usage
if __name__ == "__main__":
    calculate_borough_averages()
