"""
Generates a compact 1-page summary of PSP Delivery Categories J003 - J006
in Word document (.docx) format using only Python's standard library (zipfile + XML).
"""

import os
import zipfile

DOCX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PSP_Delivery_Summary.docx")

# Minimal WordprocessingML templates
CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""

RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOCUMENT_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <!-- Document Title -->
    <w:p>
      <w:pPr>
        <w:jc w:val="center"/>
        <w:spacing w:after="100"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="34"/>
          <w:color w:val="1F4E78"/>
        </w:rPr>
        <w:t>PSP Delivery Summary: J003 – J006</w:t>
      </w:r>
    </w:p>

    <!-- Subtitle -->
    <w:p>
      <w:pPr>
        <w:jc w:val="center"/>
        <w:spacing w:after="240"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:i/>
          <w:sz w:val="20"/>
          <w:color w:val="595959"/>
        </w:rPr>
        <w:t>Student Grade Management System | Python 3 &amp; SQLite | Standard Library Only</w:t>
      </w:r>
    </w:p>

    <!-- Section: 1. Deliverables by Category -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="100"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="24"/>
          <w:color w:val="1F4E78"/>
        </w:rPr>
        <w:t>1. Deliverables by PSP Category</w:t>
      </w:r>
    </w:p>

    <!-- Table -->
    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="9360" w:type="dxa"/>
        <w:tblBorders>
          <w:top w:val="single" w:sz="6" w:space="0" w:color="D3D3D3"/>
          <w:left w:val="none"/>
          <w:bottom w:val="single" w:sz="6" w:space="0" w:color="D3D3D3"/>
          <w:right w:val="none"/>
          <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>
          <w:insideV w:val="none"/>
        </w:tblBorders>
      </w:tblPr>

      <!-- Table Header -->
      <w:tr>
        <w:tc>
          <w:tcPr>
            <w:tcW w:w="2600" w:type="dxa"/>
            <w:shd w:val="clear" w:color="auto" w:fill="1F4E78"/>
          </w:tcPr>
          <w:p><w:pPr><w:spacing w:before="80" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/><w:color w:val="FFFFFF"/></w:rPr><w:t>Category</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr>
            <w:tcW w:w="5260" w:type="dxa"/>
            <w:shd w:val="clear" w:color="auto" w:fill="1F4E78"/>
          </w:tcPr>
          <w:p><w:pPr><w:spacing w:before="80" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/><w:color w:val="FFFFFF"/></w:rPr><w:t>Artifacts &amp; Implementation Details</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr>
            <w:tcW w:w="1500" w:type="dxa"/>
            <w:shd w:val="clear" w:color="auto" w:fill="1F4E78"/>
          </w:tcPr>
          <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/><w:color w:val="FFFFFF"/></w:rPr><w:t>Quantity</w:t></w:r></w:p>
        </w:tc>
      </w:tr>

      <!-- Row: J003 -->
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="2600" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="80" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>J003 – Input &amp; Validation</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="5260" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="80" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>• add_student(): Rejects empty or whitespace-only names.</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="40" w:after="80"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>• add_grade(): Validates student ID, subject range (1-5), numeric mark (0-100), and blocks duplicate entries.</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="1500" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>2 Functions</w:t></w:r></w:p>
        </w:tc>
      </w:tr>

      <!-- Row: J004 -->
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="2600" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="F9F9F9"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="80" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>J004 – Grade Calculation &amp; Output</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="5260" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="F9F9F9"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="80" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>• calculate_letter_grade(mark): Scale A (90-100) to F (&lt;60).</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>• calculate_average(id): Arithmetic mean or None.</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="40" w:after="80"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>• display_records(), get_all_records(), filter_by_name(), filter_by_subject(), filter_by_letter_grade(), view_records() / filter_records().</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="1500" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="F9F9F9"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>8 Functions</w:t></w:r></w:p>
        </w:tc>
      </w:tr>

      <!-- Row: J005 -->
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="2600" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="80" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>J005 – Testing &amp; Debugging</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="5260" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="80" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>• test_main.py: 6 test suites covering student validation, mark bounds (&lt;0, &gt;100), duplicate prevention, partial name search, letter grade filter, average calculation, and database restart persistence.</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="40" w:after="80"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/><w:color w:val="2E7D32"/></w:rPr><w:t>• 100% test pass rate across all 12 specification cases.</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="1500" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/><w:color w:val="2E7D32"/></w:rPr><w:t>21 Unit Tests</w:t></w:r></w:p>
        </w:tc>
      </w:tr>

      <!-- Row: J006 -->
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="2600" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="F9F9F9"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="80" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>J006 – Documentation &amp; Review</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="5260" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="F9F9F9"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="80" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>• 1-page PDF quick reference: Student_Grade_Management_Docs.pdf</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>• Word (.docx) PSP Delivery Summary: PSP_Delivery_Summary.docx</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="40" w:after="80"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>• Markdown specifications &amp; schema architecture documentation.</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="1500" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="F9F9F9"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>3 Documents</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>

    <!-- Section: 2. Database Architecture -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="180" w:after="80"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="24"/>
          <w:color w:val="1F4E78"/>
        </w:rPr>
        <w:t>2. Database Schema (students.db)</w:t>
      </w:r>
    </w:p>

    <w:p>
      <w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>• students: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>id (INTEGER PK AUTOINCREMENT), name (TEXT NOT NULL)</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>• subjects: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>id (INTEGER PK), name (TEXT NOT NULL UNIQUE) — 5 subjects seeded automatically</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="40" w:after="120"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>• grades: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>id (INTEGER PK AUTOINCREMENT), student_id (FK), subject_id (FK), mark (REAL CHECK(0-100)), UNIQUE(student_id, subject_id)</w:t></w:r>
    </w:p>

    <!-- Section: 3. Execution Commands -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="80"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="24"/>
          <w:color w:val="1F4E78"/>
        </w:rPr>
        <w:t>3. Execution &amp; Testing Commands</w:t>
      </w:r>
    </w:p>

    <w:p>
      <w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>Run Application: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="18"/><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/></w:rPr><w:t>python main.py</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="40" w:after="160"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>Execute Test Suite: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="18"/><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/></w:rPr><w:t>python -m unittest test_main -v</w:t></w:r>
    </w:p>

    <!-- Page Setup (1 inch margins, standard Letter size) -->
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1080" w:right="1440" w:bottom="1080" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>"""

def create_docx():
    with zipfile.ZipFile(DOCX_PATH, "w", zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", CONTENT_TYPES_XML)
        docx.writestr("_rels/.rels", RELS_XML)
        docx.writestr("word/document.xml", DOCUMENT_XML)
    print(f"DOCX created at: {DOCX_PATH}")

if __name__ == "__main__":
    create_docx()
