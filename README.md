# Tornado project creator

## How to use

```
python tornado-bootstrap-creator.py new_project \
    --prefix ~/Tmp \
    --package simpleweb \
    --force \
    --author leenjewel \
    --email leenjewel@gmail.com \
    --routes '/ad:ADHandler.ad;/revenue:RevenueHandler.revenue'
```

## How to run

```
cd ~/Tmp/simpleweb

python setup.py install

python ./simpleweb.py startweb
```
