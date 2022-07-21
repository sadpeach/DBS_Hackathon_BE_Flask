from hackathon import app
import os

#Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
