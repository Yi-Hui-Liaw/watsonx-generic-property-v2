import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
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
import datetime


def get_region_links(driver):
    element = driver.find_elements(By.CSS_SELECTOR, 'a.headerRegionLink')
    return element

def get_project_links(url):

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new") 
    options.add_argument("window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Locate the "Property" menu link more reliably
    property_menu = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, "//a[contains(., 'Property') and contains(@class, 'dropdown-toggle')]")
    ))

    # Click using JS to avoid hover-only interaction
    driver.execute_script("arguments[0].click();", property_menu)

    time.sleep(2)

    # Get all region links
    region_links = WebDriverWait(driver, 2).until(get_region_links)

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

        #load more
        # load_more = driver.find_elements(By.CSS_SELECTOR, '#loadMore')
        # driver.execute_script("arguments[0].click();", load_more)
        # time.sleep(1.5)

        # Find all project cards now visible (inside the region projects container)
        project_links = driver.find_elements(By.CSS_SELECTOR, '.region-projects .tab-pane.active a.s-card')
        
        for link in project_links:
            url = link.get_attribute("href")
            if url not in all_project_urls:
                print(f"  → Found project: {url}")
                all_project_urls.append(url)

    # ✅ Done
    # print(all_project_urls)
    print("Property found:")
    for project in all_project_urls:
        print(project)
    print(f"\nTotal projects found: {len(all_project_urls)}")
    driver.quit()

    return all_project_urls


async def crawl(url="https://www.uemsunrise.com"):
    start = time.process_time()
    # Execute the crawl
    project_links = get_project_links(url)
    project_links = [ r for r in project_links if 'malaysia-vision-valley' in r]
    results = []
    crawled_urls = []

    js_commands = """

    cosnt button = document.querySelector('#loadMore')?.click();
    """
    
    browser_config = BrowserConfig(
        headless=True,
        browser_type="chromium",
        # viewport_width=1920,
        # viewport_height=1080,
        verbose=True,
        user_agent_mode='random',
        text_mode=True,
     )  
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for url in project_links:
            # Create a sophisticated filter chain
            filter_chain = FilterChain([
                # URL patterns to include
                URLPatternFilter(patterns=["*property/region/malaysia-vision-valley/*"], reverse=False),
                URLPatternFilter(patterns=["*#*"]+crawled_urls, reverse=True),

                # Content type filtering
                ContentTypeFilter(allowed_types=["text/html"])
            ])

            # Create a relevance scorer
            keyword_scorer = KeywordRelevanceScorer(
                keywords=[ "project", "development","region"],
                weight=0.7
            )   

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
                scan_full_page=True,
                # js_code=js_commands,
                # js_only=True,
                wait_for="""js:() => (()=>{
                var loadMoreFn = function(){
                const lmButton = document.querySelector("#loadMore");
                    if(lmButton){
                        if(document.querySelectorAll('#loadMore')[0].style.display != 'none'){
                            lmButton.click();
                            setTimeout(loadMoreFn, 1000);
                        }
                        else{
                        return true;
                        }
                    }   
                    return true;
                }
                loadMoreFn();
                })();
                """,
                # session_id='session',
                check_robots_txt=True,
                page_timeout=60000,
            )
            print(f"\n🚀 Crawling: {url}")
            async for result in await crawler.arun(url, config=config):
                results.append(result)
                crawled_urls.append(result.url)
                score = result.metadata.get("score", 0)
                depth = result.metadata.get("depth", 0)
                print(f"Depth: {depth} | Score: {score:.2f} | {result.url}")

    # # Analyze the results
    # print(f"Crawled {len(results)} high-value pages")
    # print(f"Average score: {sum(r.metadata.get('score', 0) for r in results) / len(results):.2f}")

    # # Group by depth
    # depth_counts = {}
    # for result in results:
    #     depth = result.metadata.get("depth", 0)
    #     depth_counts[depth] = depth_counts.get(depth, 0) + 1

    # print("Pages crawled by depth:")
    # for depth, count in sorted(depth_counts.items()):
    #     print(f"  Depth {depth}: {count} pages")

    print("Crawled page")
    # crawled_urls = sorted(list(set([r.url for r in results])))
    for cu in crawled_urls:
        print("- ", cu)

    print(f"total uniqued crawled page - {len(crawled_urls)}")
    end = time.process_time()
    print("Time taken to run - ",str(datetime.timedelta(seconds=end-start)))
if __name__ == "__main__":
    asyncio.run(crawl())