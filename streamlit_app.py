"""A local-first interface for explicit email-list comparisons."""

import streamlit as st

from email_lists import compare, export_csv, read_emails

st.set_page_config(page_title="Email List Checker", page_icon="📋")
st.title("Email List Checker")
st.write("Compare two CSV email lists, review the result and download a clean export.")
st.caption("List comparison only. This tool does not verify email syntax, deliverability or consent.")

choices = {
    "Only in one list (exclude shared addresses)": "different",
    "Merge both lists (keep one copy of every address)": "merged",
    "Shared by both lists": "shared",
}
selection = st.selectbox("Comparison", list(choices))
first_file = st.file_uploader("First CSV — requires an Email column", type=["csv"], key="first")
second_file = st.file_uploader("Second CSV — requires an Email column", type=["csv"], key="second")
st.caption("UTF-8 CSV, up to 5 MB and 100,000 rows per file. Surrounding whitespace and letter case are normalized.")

if first_file is not None and second_file is not None:
    try:
        first = read_emails(first_file.getvalue())
        second = read_emails(second_file.getvalue())
        result = compare(first, second, choices[selection])
    except ValueError as error:
        st.error(str(error))
    else:
        columns = st.columns(3)
        columns[0].metric("First list — distinct addresses", len(first))
        columns[1].metric("Second list — distinct addresses", len(second))
        columns[2].metric("Shared addresses", len(first & second))
        st.write(f"Result: {len(result):,} addresses")
        st.dataframe({"Email": result}, use_container_width=True)
        st.download_button(
            "Download result CSV", data=export_csv(result), file_name="email_comparison.csv", mime="text/csv"
        )
        st.caption("Spreadsheet-sensitive values are prefixed with an apostrophe in the CSV export.")

st.info("Use data you are authorized to process. In a hosted deployment, uploads are processed on that server. Do not commit real contact lists.")
