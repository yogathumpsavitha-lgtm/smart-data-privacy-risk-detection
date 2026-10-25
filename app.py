import streamlit as st
from pathlib import Path
import tempfile

from document_processor import extract_text
from detector import detect_sensitive_data


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Data Privacy Risk Detection",
    page_icon="🔐",
    layout="wide",
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🔐 Smart Data Privacy Risk Detection")

st.write(
    "Scan documents for potentially sensitive information "
    "and review findings before sharing."
)

st.warning(
    "Upload only documents you are authorized to process. "
    "This prototype processes files locally."
)


# --------------------------------------------------
# DOCUMENT UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["txt", "pdf", "docx"],
)


# --------------------------------------------------
# PROCESS UPLOADED DOCUMENT
# --------------------------------------------------

def extract_text_from_upload(uploaded_file):

    suffix = Path(uploaded_file.name).suffix.lower()

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=suffix,
            delete=False,
        ) as temporary_file:

            temporary_file.write(
                uploaded_file.getvalue()
            )

            temporary_path = temporary_file.name

        return extract_text(temporary_path)

    finally:
        if temporary_path is not None:
            Path(temporary_path).unlink(missing_ok=True)


# --------------------------------------------------
# SCAN DOCUMENT
# --------------------------------------------------

if uploaded_file is not None:

    if st.button("🔍 Scan Document", type="primary"):

        try:
            with st.spinner("Scanning document..."):

                result = extract_text_from_upload(
                    uploaded_file
                )

                if result["status"] != "success":
                    st.error(result["message"])
                    st.stop()

                findings = detect_sensitive_data(
                    result["text"]
                )

            # Save results for the review stage.
            st.session_state["scan_text"] = result["text"]
            st.session_state["scan_findings"] = findings
            st.session_state["scan_filename"] = uploaded_file.name

            st.success("Document scanned successfully!")

        except Exception as error:
            st.error(
                f"Scanning failed: {type(error).__name__}: {error}"
            )


# --------------------------------------------------
# DISPLAY SCAN RESULTS
# --------------------------------------------------

if "scan_findings" in st.session_state:

    findings = st.session_state["scan_findings"]
    original_text = st.session_state["scan_text"]

    st.divider()

    st.header("📊 Privacy Risk Dashboard")

    total_findings = len(findings)

    high_risk_count = sum(
        1 for item in findings
        if item["risk"] == "High"
    )

    medium_risk_count = sum(
        1 for item in findings
        if item["risk"] == "Medium"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Findings",
        total_findings,
    )

    col2.metric(
        "High-Risk Findings",
        high_risk_count,
    )

    col3.metric(
        "Medium-Risk Findings",
        medium_risk_count,
    )

    st.subheader("🔎 Detected Information")

    if not findings:

        st.info(
            "No configured sensitive patterns were detected. "
            "This does not guarantee that the document is safe."
        )

    else:

        st.caption(
            "Review each finding. Detection results may include "
            "false positives and require human confirmation."
        )

        for index, item in enumerate(findings):

            with st.expander(
                f"{item['type']} — {item['risk']} Risk"
            ):

                st.write(
                    f"**Detected value:** `{item['value']}`"
                )

                st.write(
                    f"**Text position:** "
                    f"{item['start']}–{item['end']}"
                )

                st.write(
                    f"**Risk level:** {item['risk']}"
                )

                st.checkbox(
                    "Approve this finding for redaction",
                    key=f"approve_{index}",
                )


    # --------------------------------------------------
    # REDACTION PREVIEW
    # --------------------------------------------------

    st.divider()

    st.header("🛡️ Redaction Preview")

    st.write(
        "Approved findings will be masked in a separate text copy. "
        "The original uploaded document is not overwritten."
    )

    if findings:

        approved_findings = [
            item
            for index, item in enumerate(findings)
            if st.session_state.get(
                f"approve_{index}",
                False,
            )
        ]

    else:
        approved_findings = []


    # Replace approved matches from right to left
    # to preserve the original text positions.
    redacted_text = original_text

    for item in sorted(
        approved_findings,
        key=lambda finding: finding["start"],
        reverse=True,
    ):

        redacted_text = (
            redacted_text[:item["start"]]
            + "[REDACTED]"
            + redacted_text[item["end"]:]
        )


    if approved_findings:

        st.text_area(
            "Preview of redacted text",
            value=redacted_text,
            height=250,
        )

        st.download_button(
            label="⬇️ Download Redacted Text",
            data=redacted_text,
            file_name="redacted_document.txt",
            mime="text/plain",
        )

    else:

        st.info(
            "Approve at least one finding above to generate "
            "a redacted text copy."
        )


    # --------------------------------------------------
    # AUDIT SUMMARY
    # --------------------------------------------------

    st.divider()

    st.header("📋 Audit Summary")

    audit_lines = [
        "SMART DATA PRIVACY RISK DETECTION",
        f"Document: {st.session_state['scan_filename']}",
        f"Total findings: {total_findings}",
        f"High-risk findings: {high_risk_count}",
        f"Medium-risk findings: {medium_risk_count}",
        f"Approved for redaction: {len(approved_findings)}",
        "",
        "Finding details:",
    ]

    for item in findings:

        audit_lines.append(
            f"- Type: {item['type']}; "
            f"Risk: {item['risk']}; "
            f"Position: {item['start']}-{item['end']}"
        )

    audit_summary = "\n".join(audit_lines)

    st.download_button(
        label="⬇️ Download Audit Summary",
        data=audit_summary,
        file_name="privacy_audit_summary.txt",
        mime="text/plain",
    )

    st.caption(
        "This prototype uses pattern-based detection. "
        "It does not guarantee that all sensitive information "
        "has been identified or removed."
    )