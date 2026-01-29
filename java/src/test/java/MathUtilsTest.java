import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class MathUtilsTest {

  @BeforeEach
  void setup() { }

  @AfterEach
  void teardown() { }

  @Test
  void testAdd() {
    assertEquals(3, MathUtils.add(1, 2));
    assertEquals(0, MathUtils.add(-1, 1));
  }

  @Test
  void testSubtract() {
    assertEquals(3, MathUtils.subtract(5, 2));
    assertEquals(-3, MathUtils.subtract(2, 5));
  }

  @Test
  void testMultiply() {
    assertEquals(12, MathUtils.multiply(3, 4));
    assertEquals(0, MathUtils.multiply(0, 999));
  }

  @Test
  void testDivideValid() {
    assertEquals(5.0, MathUtils.divide(10, 2));
    assertEquals(-3.0, MathUtils.divide(-9, 3));
  }

  @Test
  void testDivideByZero() {
    assertEquals(-1.0, MathUtils.divide(10, 0));
    assertEquals(-1.0, MathUtils.divide(0, 0));
  }
}

