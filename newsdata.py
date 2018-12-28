# Import PostgreSQL
import psycopg2

# Setting up connection
DBNAME = "news"
db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# Question_1
with open("output.txt", "w") as outfile:
    outfile.write("""1. Three most popular articles of all time:\n""")

c.execute("""select path, count(*) as num from log group by path
order by num desc limit 3 offset 1;""")
results = c.fetchall()

with open("output.txt", "a") as outfile:
    for result in results:
        article_name = result[0]
        article_view = str(result[1])
        article_result = article_name[9:] + " => " + article_view + " views"
        outfile.write(article_result)
        outfile.write("\n")

# Question_2
with open("output.txt", "a") as outfile:
    outfile.write("""\n2. Most popular article authors of all time:\n""")

c.execute("""select authors.name, sum(views) as sum_view from authors,
(select title,author,count(*) as views from articles,log where
log.path like concat('%',articles.slug) group by articles.title,articles.author
) as view where authors.id = view.author
group by authors.name
order by sum_view desc;""")
results = c.fetchall()

with open("output.txt", "a") as outfile:
    for result in results:
        author_name = result[0]
        author_views = str(result[1])
        author_result = author_name + " => " + author_views + " views"
        outfile.write(author_result)
        outfile.write("\n")

# Question_3
with open("output.txt", "a") as outfile:
    outfile.write("""\n3. Days more than 1% of requests lead to errors? \n""")

c.execute("""select date(time),round(100.0*sum(case log.status when '200 OK'
then 0 else 1 end)/count(log.status),2) as "Percent Error"
from log group by date(time)
order by "Percent Error" desc limit 1;""")
results = c.fetchall()

with open("output.txt", "a") as outfile:
    for result in results:
        date = str(result[0])
        error_rate = str(result[1])
        outfile.write(date + " => " + error_rate + "% error rate")

db.close()
