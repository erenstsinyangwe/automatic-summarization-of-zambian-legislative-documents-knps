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
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome Summarizer-KNPS: Your Gateway to Effortless Zambian Legislative Document Summarization 👋")

    st.sidebar.success("# We have two summaries to choose from Abstractive and Extractive, and we can select the one we prefer to use ")

    st.markdown(
        """
        # Project Name: Automatic Summarisation of Zambian Legislative

        To access the desired PDF on the *National Assembly Parliament website*, simply copy the link of the PDF document you wish to download, then paste it into your chosen summarization tool and click 'extract'
    
      """
    )


if __name__ == "__main__":
    run()