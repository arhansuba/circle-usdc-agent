# main.py
import subprocess
import json
import re
from ai_research import run_research
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_circle_payment(contributions):
    """Process payments through the Circle payment system."""
    try:
        process = subprocess.Popen(
            ['node', 'circle_payment.js'], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = process.communicate(input=json.dumps(contributions).encode())
        
        if process.returncode != 0:
            logger.error(f"Error from payment service: {stderr.decode()}")
            return None

        json_output = re.search(
            r'=== JSON_OUTPUT_START ===\n(.*)\n=== JSON_OUTPUT_END ===', 
            stdout.decode(), 
            re.DOTALL
        )
        
        if json_output:
            results = json.loads(json_output.group(1))
            if results['success']:
                logger.info("All payments processed successfully.")
                for agent, payment in results['payments'].items():
                    logger.info(f"Agent: {agent}")
                    logger.info(f"  Transaction ID: {payment['transactionId']}")
                    logger.info(f"  Amount: {payment['amount']}")
                    logger.info(f"  Validated: {'Yes' if payment['validated'] else 'No'}")
            else:
                logger.error(f"Payment processing failed: {results.get('error', 'Unknown error')}")
            return results
            
        else:
            logger.error("Could not find JSON output in the response")
            return None
            
    except Exception as e:
        logger.error(f"Unexpected error in payment processing: {str(e)}")
        return None

def main():
    try:
        topic = "Artificial intelligence and employment trends"
        logger.info(f"Starting research on topic: {topic}")
        
        contributions = run_research(topic)
        logger.info("Research completed. Processing payments...")
        
        payment_result = run_circle_payment(contributions)
        
        if payment_result and payment_result['success']:
            logger.info("Payment process completed successfully.")
        else:
            logger.error("Payment process failed.")
            
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()