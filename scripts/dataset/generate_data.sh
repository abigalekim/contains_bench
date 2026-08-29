python3  generate_simple_benchmark.py skew 16 20000
python3  generate_simple_benchmark.py skew 32 20000
python3  generate_simple_benchmark.py skew 64 20000
python3 uniform_dist.py 16 128
python3 normal_dist.py 16 128
python3 bimodal_dist.py 16 5 512 100
python3 bimodal_dist.py 32 10 512 100
python3 bimodal_dist.py 64 20 512 100
python3 bimodal_dist.py 16 5 8192 500
python3 bimodal_dist.py 32 10 8192 500
python3 bimodal_dist.py 64 20 8192 500
python3 bimodal_dist.py 16 5 65536 2000
python3 bimodal_dist.py 32 10 65536 2000
python3 bimodal_dist.py 64 20 65536 2000
python3 process_fb.py
python3 process_reddit_comments.py
python3 process_twitter.py
python3 process_yelp.py
python3 process_amazon_reviews.py
python3 process_github.py
python3 process_webarchive.py