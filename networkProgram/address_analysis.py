import csv
import random
import re  # tool for working with text and validation


# Function to generate a random IPv4 address and CIDR prefix
def generate_random_subnet():
    """
    Generate a random IPv4 address with a CIDR prefix.
    Returns:
        tuple: A tuple containing a random IPv4 address as a string and a randomly selected CIDR prefix
               (either 8, 16, or 24).
    """
    # Generate random IP components for four octets
    ip_octets = [random.randint(0, 255) for _ in range(4)]
    random_ip = f"{ip_octets[0]}.{ip_octets[1]}.{ip_octets[2]}.{ip_octets[3]}"
    # Choose a random CIDR prefix length for simplicity
    cidr_prefix = random.choice([8, 16, 24])  # Limits to common A, B, C network classes
    return random_ip, cidr_prefix


# check formatting for subnet mask
def validate_subnet_mask(user_input):
    """
    Validate the subnet mask format and values.
    Args:
        user_input (str): The subnet mask entered by the user.
    Returns:
        bool: True if the format is valid, False otherwise.
    """
    # Check if the format matches XXX.XXX.XXX.XXX where X is a digit
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    if not re.match(pattern, user_input): # re.match attempts to match user_input string against pattern from beginning of string
        return False
    # Check if each octet is a valid number (0-255)
    try:
        octets = [int(x) for x in user_input.split('.')]
        return all(0 <= octet <= 255 for octet in octets)
    except ValueError:
        return False


# get formatting for address class (A / 0)
def format_address_class_pattern(user_input):
    """
    Format the address class and bit pattern input to match the required format.
    Args:
        user_input (str): The user's input for address class and bit pattern.
    Returns:
        tuple: (bool, str) - (is_valid, formatted_string)
        bool: True if input is valid, False otherwise
        str: Formatted string if valid, None if invalid
    """
    try:
        # Remove any extra spaces and split by '/'
        parts = user_input.strip().split('/')
        if len(parts) != 2:
            return False, None
        # Extract class and pattern
        address_class = parts[0].strip().upper()
        bit_pattern = parts[1].strip()
        # Validate address class is A, B, C, D, or E
        if address_class not in ['A', 'B', 'C', 'D', 'E']:
            return False, None
        # Validate bit pattern contains only 0s and 1s
        if not all(bit in '01' for bit in bit_pattern):
            return False, None
        # Format with proper spacing
        formatted = f"{address_class} / {bit_pattern}"
        return True, formatted
    except Exception:
        return False, None


# Function to calculate answers based on the generated IP and CIDR
def calculate_answers(ip, cidr_prefix):
    """
    Calculate networking information based on the given IP and CIDR prefix.
    Args:
        ip (str): The IP address in string format (e.g., "192.168.1.1").
        cidr_prefix (int): The CIDR prefix length (e.g., 24 for a /24 network).
    Returns:
        dict: A dictionary containing networking information.
    """
    first_octet = int(ip.split('.')[0])
    # Determine Address Class and Leading Bit Pattern
    if first_octet < 128:
        address_class = "A"
        leading_bit_pattern = "0"
    elif first_octet < 192:
        address_class = "B"
        leading_bit_pattern = "10"
    elif first_octet < 224:
        address_class = "C"
        leading_bit_pattern = "110"
    else:
        address_class, leading_bit_pattern = "D/E", "1110" if first_octet < 240 else "1111"
    # Calculate Subnet Mask
    subnet_mask_bits = '1' * cidr_prefix + '0' * (32 - cidr_prefix)
    subnet_mask_octets = [int(subnet_mask_bits[i:i+8], 2) for i in range(0, 32, 8)]
    subnet_mask = ".".join(map(str, subnet_mask_octets))
    # Split IP into octets and convert each to binary
    ip_octets = list(map(int, ip.split('.')))
    ip_binary = ''.join(f"{octet:08b}" for octet in ip_octets)
    # Network part: first `cidr_prefix` bits, Host part: remaining bits
    network_bits_binary = ip_binary[:cidr_prefix]
    host_bits_binary = ip_binary[cidr_prefix:]
    # Ensure host portion is extracted correctly based on CIDR prefix
    if cidr_prefix == 8:
        host_bits_binary = ip_binary[8:]
    return {
        "Address Class and Leading Bit Pattern": f"{address_class} / {leading_bit_pattern}",
        "Prefix Length": str(cidr_prefix),
        "Host Address in Binary": host_bits_binary,
        "Network Bits in Binary": network_bits_binary,
        "Subnet Mask": subnet_mask,
        "Number of Host Bits": str(32 - cidr_prefix),
        "Number of Network Bits": str(cidr_prefix),
    }


# Function to log the question, answer, user response, and result
def log_result(question, correct_answer, user_answer):
    """
    Log the question, correct answer, user answer, and result to a CSV file.
    Args:
        question (str): The question that was asked.
        correct_answer (str): The correct answer to the question.
        user_answer (str): The answer provided by the user.
    Returns:
        str: "Correct" if the user's answer matches the correct answer, otherwise "Incorrect".
    """
    result = "Correct" if user_answer.strip() == correct_answer.strip() else "Incorrect"
    with open("classfullAddress.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([question, correct_answer, user_answer, result])
    return result


# Main function to run the Classful Address Analysis option with random subnet
def classful_address_analysis():
    """
    Main function to perform Classful Address Analysis.
    """
    while True:
        # Generate a random subnet and calculate answers
        ip, cidr_prefix = generate_random_subnet()
        answers = calculate_answers(ip, cidr_prefix)
        # Prepare questions based on generated subnet
        questions = {
            f"Enter Address Class and leading Bit Pattern (separate by '/', e.g. 'A / 0') for {ip}/{cidr_prefix}": answers["Address Class and Leading Bit Pattern"],
            f"What is the prefix Length for {ip}/{cidr_prefix}?": answers["Prefix Length"],
            f"What is the host address in binary for {ip}/{cidr_prefix}?": answers["Host Address in Binary"],
            f"Enter network bits in binary for {ip}/{cidr_prefix}": answers["Network Bits in Binary"],
            f"How many Host bits are in {ip}/{cidr_prefix}?": answers["Number of Host Bits"],
            f"What is the Subnet Mask for {ip}/{cidr_prefix}?": answers["Subnet Mask"],
        }
        # Pick a random question
        question, correct_answer = random.choice(list(questions.items()))
        # Display question and get user input
        print("\n" + question)
        # Special handling for different question types
        if "Address Class and leading Bit Pattern" in question:
            while True:
                user_answer = input("Your Answer (format: X / Y, e.g., 'A / 0'): ")
                is_valid, formatted_answer = format_address_class_pattern(user_answer)
                if is_valid:
                    user_answer = formatted_answer
                    break
                print("Error: Please enter the address class and bit pattern in the format 'X / Y' where X is A, B, C, D, or E and Y is the bit pattern (e.g., 'A / 0')")
        elif "Subnet Mask" in question:
            while True:
                user_answer = input("Your Answer (format: XXX.XXX.XXX.XXX): ")
                if validate_subnet_mask(user_answer):
                    break
                print("Error: Please enter the subnet mask in the format XXX.XXX.XXX.XXX (e.g., 255.255.0.0)")
        else:
            user_answer = input("Your Answer: ")
        # Log the result to the CSV
        result = log_result(question, correct_answer, user_answer)
        # Give feedback to the user
        if result == "Correct":
            print("Congratulations! You got it right.")
        else:
            print(f"Sorry, the correct answer is: {correct_answer}")
        # Menu options after answering
        print("\nWould you like to:")
        print("1. Try another Classful Address Analysis question")
        print("2. Return to Main Menu")
        choice = input("Enter 1 or 2: ")
        while choice != "1" and choice != "2":
            print("\nERROR! Please enter 1 or 2.")
            choice = input("Enter 1 or 2: ")
        if choice == "2":
            break


# Initialize CSV file with headers if it doesn't exist
with open("classfullAddress.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Question", "Correct Answer", "User Answer", "Result"])
