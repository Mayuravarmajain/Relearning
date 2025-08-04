import streamlit as st
import requests
import ast

st.title("📄 Relearning Demo")

stage = st.selectbox("Select Stage", ["BRM", "OCR", "TOC", "SKEW", "SPLIT", "EXTRACT", "L-1"])

if stage == "L-1":
    pattern_input = st.text_input(
        "Enter Pattern Name",
        placeholder="Please enter pattern name like ['pattern1', 'pattern2']"
    )
else:
    pattern_input = st.text_input(
        "Enter DOCID",
        placeholder="Please enter DOCID in the form of list like ['docid1', 'docid2']"
    )

if st.button("Submit"):
    if pattern_input:
        try:
            parsed_input = ast.literal_eval(pattern_input)
            if not isinstance(parsed_input, list):
                raise ValueError("Not a list")

            with st.spinner("Checking and performing relearning..."):

                for item in parsed_input:
                    # Send to backend for each docid or pattern
                    response = requests.post(
                        "http://localhost:5000/check", data={"pattern": item, "stage": stage}
                    )
                    result = response.json()

                    relearn_response = requests.post(
                        "http://localhost:5000/relearn", data={"pattern": item, "stage": stage}
                    )
                    relearn_result = relearn_response.json()

                    if relearn_result["status"] == "success":
                        st.success(f"{item}: {relearn_result['message']}")
                    else:
                        st.error(f"{item}: {relearn_result['message']}")

        except Exception:
            st.error("❌ Please enter input in correct list format like ['value1', 'value2']")
    else:
        st.warning("⚠️ Please enter the required input.")
