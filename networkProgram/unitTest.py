import unittest
from address_analysis import (
    generate_random_subnet,
    calculate_answers,
    validate_subnet_mask,
    format_address_class_pattern
)

# Create a class that contains all our tests
class TestAddressAnalysis(unittest.TestCase):
    
    def test_generate_random_subnet(self):
        """
        This test makes sure our function creates valid IP addresses
        A valid IP address should:
        - Have 4 numbers separated by dots
        - Each number should be between 0 and 255
        - The CIDR prefix should be either 8, 16, or 24
        """
        print("\nTesting IP address generation...")
        
        # Generate an IP address and CIDR prefix
        ip, cidr = generate_random_subnet()
        
        # Split the IP address into its parts (called octets)
        parts = ip.split('.')
        
        # Test 1: Check if we have exactly 4 parts
        print(f"Generated IP: {ip}")
        self.assertEqual(len(parts), 4, "IP address should have exactly 4 numbers")
        
        # Test 2: Check if each part is a valid number (0-255)
        for part in parts:
            number = int(part)
            print(f"Checking if {number} is between 0 and 255")
            self.assertTrue(0 <= number <= 255)
        
        # Test 3: Check if CIDR is valid
        print(f"Checking if CIDR {cidr} is valid")
        self.assertTrue(cidr in [8, 16, 24], "CIDR should be 8, 16, or 24")

    def test_calculate_answers(self):
        """
        This test checks if our program correctly calculates networking information
        We'll test with known IP addresses and verify the results
        """
        print("\nTesting network calculations...")
        
        # Test with a Class A address (starts with number < 128)
        print("\nTesting Class A address...")
        answers = calculate_answers("10.0.0.1", 8)
        
        # Check if the answers are correct
        print("Checking Class A results...")
        self.assertEqual(answers["Address Class and Leading Bit Pattern"], "A / 0")
        self.assertEqual(answers["Subnet Mask"], "255.0.0.0")
        
        # Test with a Class B address (starts with number between 128 and 191)
        print("\nTesting Class B address...")
        answers = calculate_answers("172.16.0.1", 16)
        
        # Check if the answers are correct
        print("Checking Class B results...")
        self.assertEqual(answers["Address Class and Leading Bit Pattern"], "B / 10")
        self.assertEqual(answers["Subnet Mask"], "255.255.0.0")

    def test_validate_subnet_mask(self):
        """
        This test checks if our program can correctly identify valid and invalid subnet masks
        """
        print("\nTesting subnet mask validation...")
        
        # List of subnet masks that should be valid
        valid_masks = [
            "255.0.0.0",
            "255.255.0.0",
            "255.255.255.0"
        ]
        
        # Test valid subnet masks
        print("Testing valid subnet masks...")
        for mask in valid_masks:
            print(f"Checking valid mask: {mask}")
            self.assertTrue(validate_subnet_mask(mask))
        
        # List of subnet masks that should be invalid
        invalid_masks = [
            "256.0.0.0",    # 256 is too high (max is 255)
            "255.0.0",      # Missing a number
            "abc.0.0.0",    # Contains letters
            ""             # Empty string
        ]
        
        # Test invalid subnet masks
        print("Testing invalid subnet masks...")
        for mask in invalid_masks:
            print(f"Checking invalid mask: {mask}")
            self.assertFalse(validate_subnet_mask(mask))

    def test_format_address_class_pattern(self):
        """
        This test checks if our program correctly formats the address class and pattern
        Example: converting "b/10" to "B / 10"
        """
        print("\nTesting address class formatting...")
        
        # Test cases with input and expected output
        test_cases = [
            # (input, should_be_valid, expected_output)
            ("a/0", True, "A / 0"),
            ("B/10", True, "B / 10"),
            ("c/110", True, "C / 110")
        ]
        
        # Test each case
        for input_text, should_be_valid, expected_output in test_cases:
            print(f"\nTesting input: {input_text}")
            is_valid, formatted_text = format_address_class_pattern(input_text)
            
            # Check if the validation is correct
            print(f"Checking if validation is correct (should be {should_be_valid})")
            self.assertEqual(is_valid, should_be_valid)
            
            # If it should be valid, check if the formatting is correct
            if should_be_valid:
                print(f"Checking if format is correct (should be {expected_output})")
                self.assertEqual(formatted_text, expected_output)
        
        # Test invalid inputs
        invalid_inputs = [
            "F/0",      # F is not a valid class
            "A/2",      # 2 is not a valid bit pattern
            "A",        # Missing the pattern
            "",        # Empty string
        ]
        
        print("\nTesting invalid inputs...")
        for invalid_input in invalid_inputs:
            print(f"Testing invalid input: {invalid_input}")
            is_valid, formatted = format_address_class_pattern(invalid_input)
            self.assertFalse(is_valid, f"Input should be invalid: {invalid_input}")


if __name__ == '__main__':
    unittest.main(verbosity=2)