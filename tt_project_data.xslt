<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <title>Job Listings</title>
        <style>
          /* Add CSS styles for the webpage */
          /* Example: */
          body {
            font-family: Arial, sans-serif;
          }
          h1 {
            color: #333;
          }
          table {
            border-collapse: collapse;
            width: 100%;
          }
          th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
          }
          th {
            background-color: #f2f2f2;
          }
          .logo {
            max-width: 80px;
            max-height: 80px;
          }
        </style>
      </head>
      <body>
        <h1>Job Listings</h1>
        <table>
          <tr>
            <th>Company</th>
            <th>Location</th>
            <th>Company Size</th>
            <th>Company Type</th>
            <th>Company Sector</th>
            <th>Company Industry</th>
            <th>Company Founded</th>
            <th>Company Revenue</th>
            <th>Monthly Salary</th>
            <th>Number</th>
            <th>Job Title</th>
            <th>Experience Level</th>
          </tr>
          <xsl:for-each select="data/item">
            <tr>
              <td><xsl:value-of select="company"/></td>
              <td><xsl:value-of select="location"/></td>
              <td><xsl:value-of select="company_size"/></td>
              <td><xsl:value-of select="company_type"/></td>
              <td><xsl:value-of select="company_sector"/></td>
              <td><xsl:value-of select="company_industry"/></td>
              <td><xsl:value-of select="company_founded"/></td>
              <td><xsl:value-of select="company_revenue"/></td>
              <td><xsl:value-of select="monthly_salary"/></td>
              <td><xsl:value-of select="number"/></td>
              <td><xsl:value-of select="job_title"/></td>
              <td><xsl:value-of select="experience_level"/></td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
