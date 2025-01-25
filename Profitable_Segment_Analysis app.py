{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "daaedfc0-dd68-4460-8d2f-4da6c9efb92a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__'\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n",
      " * Running on all addresses (0.0.0.0)\n",
      " * Running on http://127.0.0.1:5051\n",
      " * Running on http://192.168.1.39:5051\n",
      "Press CTRL+C to quit\n",
      " * Restarting with watchdog (fsevents)\n",
      "0.00s - Debugger warning: It seems that frozen modules are being used, which may\n",
      "0.00s - make the debugger miss breakpoints. Please pass -Xfrozen_modules=off\n",
      "0.00s - to python to disable frozen modules.\n",
      "0.00s - Note: Debugging will proceed. Set PYDEVD_DISABLE_FILE_VALIDATION=1 to disable this validation.\n",
      "Traceback (most recent call last):\n",
      "  File \"/opt/anaconda3/lib/python3.11/site-packages/ipykernel_launcher.py\", line 17, in <module>\n",
      "    app.launch_new_instance()\n",
      "  File \"/opt/anaconda3/lib/python3.11/site-packages/traitlets/config/application.py\", line 991, in launch_instance\n",
      "    app.initialize(argv)\n",
      "  File \"/opt/anaconda3/lib/python3.11/site-packages/traitlets/config/application.py\", line 113, in inner\n",
      "    return method(app, *args, **kwargs)\n",
      "           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
      "  File \"/opt/anaconda3/lib/python3.11/site-packages/ipykernel/kernelapp.py\", line 654, in initialize\n",
      "    self.init_sockets()\n",
      "  File \"/opt/anaconda3/lib/python3.11/site-packages/ipykernel/kernelapp.py\", line 331, in init_sockets\n",
      "    self.shell_port = self._bind_socket(self.shell_socket, self.shell_port)\n",
      "                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
      "  File \"/opt/anaconda3/lib/python3.11/site-packages/ipykernel/kernelapp.py\", line 253, in _bind_socket\n",
      "    return self._try_bind_socket(s, port)\n",
      "           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
      "  File \"/opt/anaconda3/lib/python3.11/site-packages/ipykernel/kernelapp.py\", line 229, in _try_bind_socket\n",
      "    s.bind(\"tcp://%s:%i\" % (self.ip, port))\n",
      "  File \"/opt/anaconda3/lib/python3.11/site-packages/zmq/sugar/socket.py\", line 302, in bind\n",
      "    super().bind(addr)\n",
      "  File \"zmq/backend/cython/socket.pyx\", line 564, in zmq.backend.cython.socket.Socket.bind\n",
      "  File \"zmq/backend/cython/checkrc.pxd\", line 28, in zmq.backend.cython.checkrc._check_rc\n",
      "zmq.error.ZMQError: Address already in use (addr='tcp://127.0.0.1:55949')\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[0;31mSystemExit\u001b[0m\u001b[0;31m:\u001b[0m 1\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/opt/anaconda3/lib/python3.11/site-packages/IPython/core/interactiveshell.py:3561: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, render_template, request, jsonify\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import io\n",
    "import base64\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "# Load dataset (ensure 'merged_dataset.csv' is in the same directory or provide full path)\n",
    "data = pd.read_csv('merged_dataset.csv')\n",
    "\n",
    "# Fill missing values\n",
    "def fill_missing(col):\n",
    "    if col.dtypes != 'O':\n",
    "        return col.fillna(col.median())\n",
    "    else:\n",
    "        return col.fillna(col.mode()[0])\n",
    "\n",
    "data = data.apply(fill_missing, axis=0)\n",
    "\n",
    "# Define a route for the homepage\n",
    "@app.route('/')\n",
    "def home():\n",
    "    return \"<h1>Welcome to the Flask App</h1><p>Endpoints available:</p><ul><li>/data-summary</li><li>/visualization</li></ul>\"\n",
    "\n",
    "# Define a route to return a data summary\n",
    "@app.route('/data-summary')\n",
    "def data_summary():\n",
    "    summary = data.describe().to_html()\n",
    "    return f\"<h1>Data Summary</h1>{summary}\"\n",
    "\n",
    "# Define a route for visualization\n",
    "@app.route('/visualization')\n",
    "def visualization():\n",
    "    # Example visualization: Boxplot of 'Purchase' by 'City_Category'\n",
    "    plt.figure(figsize=(10, 5))\n",
    "    sns.boxplot(x='City_Category', y='Purchase', data=data)\n",
    "    plt.title('Purchase Distribution by City Category')\n",
    "    \n",
    "    # Save the plot to a BytesIO object and encode it as a base64 string\n",
    "    img = io.BytesIO()\n",
    "    plt.savefig(img, format='png')\n",
    "    img.seek(0)\n",
    "    plot_url = base64.b64encode(img.getvalue()).decode()\n",
    "\n",
    "    return f'<h1>Visualization</h1><img src=\"data:image/png;base64,{plot_url}\" />'\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True, host='0.0.0.0', port=5051)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a4fc6304-ca4e-426d-9920-886bb2b2dc79",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
