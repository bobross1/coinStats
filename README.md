# coinStats
Automatically collect and display data about cryptocurrencies.

## live version on http://198.211.120.19

Build image: `docker build -t coinstats .` <br>
Start container: `docker run -p 8501:8501 coinstats` (now visitable on localhost) <br>

A cronjob is scheduled to update the data.