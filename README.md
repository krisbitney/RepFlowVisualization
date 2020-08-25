# Reputation Visualization
Visualize distribution of dOrg member reputation

Temporarily hosted at: https://dorg-rep-flow-visualizer.onrender.com/

Time: ~10 hours

# Local Setup
Requires python >= 3.7

1. Download repo (e.g. "git clone https://github.com/krisbitney/RepFlowVisualization.git")
2. navigate to repo folder in terminal
3. run "pip install --upgrade -r requirements.txt"
4. run "python app/server.py serve"
5. Navigate to localhost:8000 in browser

Note that these instructions assume:
* "python" is an alias for python 3.x.
* "pip" is an alias for a python 3.x pip installation.

If you have Python 2.x and Python 3.x installed, steps 3 and 4 may need to be:
 * "pip3 install --upgrade -r requirements.txt"
 * "python3 app/server.py serve"

This app was tested with Python 3.7.4 on Windows and a Debian-based linux distribution. 

Linux users may need to update gcc (http://gcc.gnu.org/).
You can update gcc on Debian-based distributions by running "apt-get update && apt-get install gcc".

Please let me know if you have issues with installation.

# To Do
* Implement features to simulate future reputation distributions
  * Make slider to respond to events and change data (e.g. https://github.com/seiyria/bootstrap-slider + Plotly.react())
  * Make it possible for users to set parameters, such as the rate of reputation accumulation and estimated FTE of each member
* Format charts so everything looks pretty
* Display sortable table of member addresses and reputation?
* Host app on Render, Heroku, or other

#### Notes
It would be ideal to forecast future reputation using past reputation trends, including reputation mints/burns, hours worked per member, and so on.

dorgjelli: "@krisbit If you're using the GraphQL schema in the DAOstack subgraph, it looks like the only field you have available to do this is txHash. You could take that txHash, and query a node to get the receipt of that tx, which has the block number in it. The block number can then be turned into a date + time.
Using ethers.js, you can get the tx receipt like so: https://docs.ethers.io/v5/api/providers/provider/#Provider-waitForTransaction

And turn the block number into a date + time like so: https://docs.ethers.io/v5/api/providers/provider/#Provider-getBlock

The Block type has a timestamp field: https://docs.ethers.io/v5/api/providers/types/#providers-Block"
