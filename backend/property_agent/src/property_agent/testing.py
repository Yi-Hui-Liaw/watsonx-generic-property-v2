# import asyncio
# from crawl4ai import AsyncWebCrawler
# from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
# from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, DFSDeepCrawlStrategy, BestFirstCrawlingStrategy
# from crawl4ai.deep_crawling.filters import (
#     FilterChain,
#     DomainFilter,
#     URLPatternFilter,
#     ContentTypeFilter,
#     ContentRelevanceFilter
# )
# from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer

# # Create a scorer


# async def main():
#     browser_config = BrowserConfig(
#         # headless=False
#      )  # Default browser configuration

#     crawl_filter = URLPatternFilter(patterns=["*property/region*"])
    
#     scorer = KeywordRelevanceScorer(
#     keywords=["property","unit","project","development", "sqft"],
#     weight=0.7
#     )

#     # strategy = DFSDeepCrawlStrategy(
#     # max_depth=6,               # Crawl initial page + 2 levels deep
#     # include_external=False,    # Stay within the same domain
#     # # max_pages=30,              # Maximum number of pages to crawl (optional)
#     # # url_scorer=scorer,     # Minimum score for URLs to be crawled (optional)
#     # # score_threshold=0.1,
#     # filter_chain=FilterChain([crawl_filter])
#     # )
    
#     # strategy = BFSDeepCrawlStrategy(
#     #     max_depth=5,               # Crawl initial page + 2 levels deep
#     #     include_external=False,    # Stay within the same domain
#     #     # max_pages=30,              # Maximum number of pages to crawl (optional)
#     #     url_scorer=scorer,
#     #     score_threshold=0.1,       # Minimum score for URLs to be crawled (optional)
#     #     filter_chain=FilterChain([crawl_filter])
#     # )
    
#     strategy = BestFirstCrawlingStrategy(
#     max_depth=5,
#     include_external=False,
#     url_scorer=scorer,
#     max_pages=30,              # Maximum number of pages to crawl (optional)
# )
    
#     config = CrawlerRunConfig(
#     deep_crawl_strategy=strategy,
#     stream=False  # Default behavior
#     )

#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         # Wait for ALL results to be collected before returning
#         results = await crawler.arun('https://www.uemsunrise.com/', config=config)
#         print('result')
#         for result in results:
#             print(result.url, result.success, result.metadata.get("score", 0))

# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import (
    FilterChain,
    DomainFilter,
    URLPatternFilter,
    ContentTypeFilter
)
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

async def run_advanced_crawler():
    # Create a sophisticated filter chain
    filter_chain = FilterChain([
        # URL patterns to include
        URLPatternFilter(patterns=["*property/region*"]),

        # Content type filtering
        ContentTypeFilter(allowed_types=["text/html"])
    ])

    # Create a relevance scorer
    keyword_scorer = KeywordRelevanceScorer(
        keywords=["sqft", "project", "development"],
        weight=0.7
    )   

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new") 
    options.add_argument("window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    driver.get("https://www.uemsunrise.com")

    # Locate the "Property" menu link more reliably
    property_menu = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//a[contains(., 'Property') and contains(@class, 'dropdown-toggle')]")
    ))

    # Click using JS to avoid hover-only interaction
    driver.execute_script("arguments[0].click();", property_menu)

    time.sleep(2)

    # Get all region links
    region_links = driver.find_elements(By.CSS_SELECTOR, 'a.headerRegionLink')

    all_project_urls = []
    
    # Process each region link dynamically
    for region_link in region_links:
        region_name = region_link.text.strip()
        region_type = region_link.get_attribute("data-type")
        
        print(f"Processing region: {region_name} ({region_type})")

        # Click region using JS to trigger the page’s native JS
        driver.execute_script("arguments[0].click();", region_link)

        # Wait for content to load — we assume some project cards will appear
        time.sleep(1.5)  # or use WebDriverWait if DOM mutation is slower

        # Find all project cards now visible (inside the region projects container)
        project_links = driver.find_elements(By.CSS_SELECTOR, '.region-projects .tab-pane.active a.s-card')
        
        for link in project_links:
            url = link.get_attribute("href")
            if url not in all_project_urls:
                print(f"  → Found project: {url}")
                all_project_urls.append(url)

    print(all_project_urls)
    print(f"\nTotal projects found: {len(all_project_urls)}")
    driver.quit()


    # js_code = ["""
    #             (() => {
    #             const propertyTab = Array.from(document.querySelectorAll('a.nav-link')).find(link => link.textContent.includes('Property'));
                    
    #             if (propertyTab) {
    #                 propertyTab.click();
                    
    #                 setTimeout(() => {
    #                 const regionLinks = document.querySelectorAll('.headerRegionLink');
                    
    #                 regionLinks.forEach((link, index) => {
    #                     setTimeout(() => {
    #                     link.click();
    #                     }, index * 500);
    #                 });
    #                 }, 1000);
    #             }
    #             })();
    # """]

    # Set up the configuration
    config = CrawlerRunConfig(
        deep_crawl_strategy=BestFirstCrawlingStrategy(
            max_depth=2,
            include_external=False,
            filter_chain=filter_chain,
            url_scorer=keyword_scorer
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        stream=True,
        verbose=True,
        #js_code=js_code
        #wait_for=js_code
    )

    # Execute the crawl
    results = []
    async with AsyncWebCrawler() as crawler:
        for url in all_project_urls:
            print(f"\n Crawling: {url}")
            async for result in await crawler.arun(url, config=config):
                results.append(result)
                score = result.metadata.get("score", 0)
                depth = result.metadata.get("depth", 0)
                print(f"Depth: {depth} | Score: {score:.2f} | {result.url}")

    # Analyze the results
    print(f"Crawled {len(results)} high-value pages")
    print(f"Average score: {sum(r.metadata.get('score', 0) for r in results) / len(results):.2f}")

    # Group by depth
    depth_counts = {}
    for result in results:
        depth = result.metadata.get("depth", 0)
        depth_counts[depth] = depth_counts.get(depth, 0) + 1

    print("Pages crawled by depth:")
    for depth, count in sorted(depth_counts.items()):
        print(f"  Depth {depth}: {count} pages")

if __name__ == "__main__":
    asyncio.run(run_advanced_crawler())
