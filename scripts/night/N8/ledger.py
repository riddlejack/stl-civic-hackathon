import duckdb
R='.'
con=duckdb.connect('n8.duckdb')
con.execute(f"""create or replace table led as select CITYBLOCK cb, HANDLE handle, PARCEL parcel, PROPERTYTYPE ptype, try_cast(SERVICEAMOUNT as double) amt,
 try_strptime(SERVICEDATE, ['%Y-%m-%d %H:%M:%S.%g','%Y-%m-%d %H:%M:%S'])::date sdate, SERVICETYPE stype, LASTDATE lastdate, LEGACY legacy
 from read_csv('{R}/data/raw/stlouis-mo.gov/files/forestry-service-records.csv', all_varchar=true, header=true)""")
print(con.execute("select count(*), min(sdate), max(sdate), count(distinct handle) from led").fetchall())
print(con.execute("select stype, count(*) from led group by 1 order by 2 desc").fetchall())
print(con.execute("select year(sdate) y, count(*), count(distinct handle), sum(case when stype in ('Grass Maint','Weed-Grass') then 1 else 0 end) cut_rows, count(distinct case when stype in ('Grass Maint','Weed-Grass') then handle end) cut_parcels from led group by 1 order by 1").fetchall())
# LRA inventory (land bank parcels), used by lra.py
con.execute(f"create or replace table lra as select * from read_csv('{R}/data/raw/stlouis-mo.gov/files/LRA_INVENTORY.csv', all_varchar=true, header=true)")
print('lra', con.execute('select count(*), count(distinct ParcelId) from lra').fetchall())
