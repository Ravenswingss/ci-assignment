package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MathUtilsTest {

    @Test
    void testAdd() {
        assertEquals(5, MathUtils.add(2, 3));
    }

    @Test
    void testSubtract() {
        assertEquals(-1, MathUtils.subtract(2, 3));
    }

    @Test
    void testMultiply() {
        assertEquals(6, MathUtils.multiply(2, 3));
    }

    @Test
    void testDivide() {
        assertEquals(2.0, MathUtils.divide(6, 3));
    }

    @Test
    void testDivideByZero() {
        assertEquals(-1.0, MathUtils.divide(6, 0));
    }
}
