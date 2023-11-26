# crawler
crawler
Personal Web Scraping Hobby Project fro feeding local ChatGPT


# Scraping Sub-Subcategories on the Homepage of http://bbs.huasing.net/sForum/bbs.php?B=147 (狮城财经)

This script is designed to extract links from the sub-subcategories on the homepage of the 狮城财经. It then uses multithreading to distribute these links to a Web Driver for HTML retrieval.

## Usage Steps:

1. **Visit the Sub-Subcategories on the Homepage:**

   Open the [Lion City Finance forum sub-subcategories homepage](http://bbs.huasing.net/sForum/bbs.php?B=147) in your browser.

2. **Retrieve Links for Each Topic:**

   Run the script, which will visit the sub-subcategories homepage and extract the links for each topic.

3. **Distribute to Web Driver for HTML Retrieval:**

   The script will chunk the collected links based on the specified worker count. These chunks will be assigned to a Web Driver for parallel HTML retrieval.

4. **Clean HTML Data:**

   Utilize the provided script to clean the obtained HTML data for further processing or analysis.
