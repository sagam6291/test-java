import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Duration;
import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.*;
import org.openqa.selenium.support.ui.*;

public class YoutubeMoviesShowMoreNavigationTest {
    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeEach
    void setUp() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new");
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--window-size=1920,1080");
        driver = new ChromeDriver(options);
        wait = new WebDriverWait(driver, Duration.ofSeconds(20));
    }

    @AfterEach
    void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    private void captureScreenshot(String name) {
        try {
            File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
            Files.copy(src.toPath(), Paths.get(name + ".png"));
        } catch (Exception e) {
            System.err.println("Screenshot failed: " + e.getMessage());
        }
    }

    @Test
    void testMoviesShowMoreNavigation() {
        try {
            driver.get("https://www.youtube.com/");
            wait.until(ExpectedConditions.titleContains("YouTube"));

            By moviesLocator = By.xpath("//tp-yt-paper-item[.//yt-formatted-string[normalize-space(text())='Movies'] or normalize-space(.)='Movies']");
            WebElement moviesItem = wait.until(ExpectedConditions.elementToBeClickable(moviesLocator));
            moviesItem.click();

            wait.until(ExpectedConditions.urlContains("/feed/storefront"));
            wait.until(ExpectedConditions.titleContains("Movies"));

            Assertions.assertTrue(driver.getCurrentUrl().contains("/feed/storefront"), "Expected URL to contain /feed/storefront");
            Assertions.assertTrue(driver.getTitle().contains("Movies"), "Expected page title to contain 'Movies'");

            By showMoreLocator = By.xpath("//tp-yt-paper-item[.//yt-formatted-string[normalize-space(text())='Show more'] or normalize-space(.)='Show more']");
            WebElement showMoreItem = wait.until(ExpectedConditions.elementToBeClickable(showMoreLocator));
            showMoreItem.click();

            wait.until(ExpectedConditions.titleContains("Movies"));
            Assertions.assertTrue(driver.getCurrentUrl().contains("/feed/storefront"), "Should remain on storefront after Show more");
        } catch (Exception e) {
            captureScreenshot("youtube_movies_show_more_failure");
            Assertions.fail("Test failed: " + e.getMessage());
        }
    }
}