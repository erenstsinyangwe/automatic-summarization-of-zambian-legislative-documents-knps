Skip to content
erenstsinyangwe
/
automatic-summarization-of-zambian-legislative-documents-knps

Type / to search

Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Commit
Update Hello.py
 main
@erenstsinyangwe
erenstsinyangwe committed 18 hours ago 
1 parent 2b4ce69
commit a3e40bd
Showing 1 changed file with 53 additions and 30 deletions.
 83 changes: 53 additions & 30 deletions83  
Hello.py
@@ -1,42 +1,65 @@
# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)
def run():
  """
  Runs the Summarizer-KNPS app.
  """

  # Page configuration
  st.set_page_config(
      page_title="Summarizer-KNPS",
      page_icon="📜"
  )

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )
  # Set the background color to a light blue
  st.markdown(
      """
      <style>
      body {
          background-color: #ADD8E6;
      }
      </style>
      """,
      unsafe_allow_html=True
  )

  # Topbar
  st.title("Summarizer-KNPS: Your Gateway to Effortless Zambian Legislative Document Summarization")

  # Type of summary selection
  summarization_type = st.selectbox(
      "Select the type of summary:",
      ["Abstractive", "Extractive"]
  )

  # Instructions
  st.markdown(
      """
      **How to use Summarizer-KNPS:**
    st.write("# Welcome Summarizer-KNPS: Your Gateway to Effortless Zambian Legislative Document Summarization 👋")
      1. Visit the [National Assembly Parliament website](https://www.parliament.gov.zm/acts-of-parliament) and find the PDF document you want to summarize.
      2. Copy the link to the PDF document.
      3. Select the type of summary.
      4. Paste the link into the Summarizer-KNPS interface and select the type of summary you want.
      5. Click the "Summarize" button.
      6. Read the summary!
    st.sidebar.success("# We have two summaries to choose from Abstractive and Extractive, and we can select the one we prefer to use ")
      **Benefits of using Summarizer-KNPS:**
    st.markdown(
        """
        # Project Name: Automatic Summarisation of Zambian Legislative
      - Save time by automatically summarizing long and complex legislative documents.
      - Better understand the key points of legislative documents.
      - Identify key trends and patterns in legislative documents.
      - Make informed decisions about Zambian legislation.
        To access the desired PDF on the *National Assembly Parliament website*, simply copy the link of the PDF document you wish to download, then paste it into your chosen summarization tool and click 'extract'
    
      **Try Summarizer-KNPS today and stay informed about Zambian legislation!**
      """
    )
  )

  # Navigation based on user's selection
  if summarization_type == "Abstractive":
      st.markdown("You can navigate to the Abstractive page [here](pages/Abstractive.py).")
  elif summarization_type == "Extractive":
      st.markdown("You can navigate to the Extractive page [here](pages/Extractive.py).")

if __name__ == "__main__":
    run()
  run()
0 comments on commit a3e40bd
@erenstsinyangwe
 
Leave a comment
No file chosen
Attach files by dragging & dropping, selecting or pasting them.
Footer
© 2023 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
Update Hello.py · erenstsinyangwe/automatic-summarization-of-zambian-legislative-documents-knps@a3e40bd
