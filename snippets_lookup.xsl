<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template name="get_snippet_id">
<!-- Returns a UUID corresponding to a snippet -->
    <xsl:param name="text"/>
    <xsl:param name="current_node_id"/>
    <xsl:variable name="stripped_text" select="normalize-space($text)"/>

    <xsl:choose>
      <xsl:when test="starts-with($stripped_text,'Significant defects addressed')">UUID-0000017c-ec46-d391-ab7f-fec787a60000</xsl:when>
      <xsl:when test="starts-with($stripped_text,'Significant improvements')">UUID-00000183-13c9-d665-af9b-fbd95d500000</xsl:when>
      <xsl:when test="starts-with($stripped_text,'Significant new feature')">UUID-00000187-0033-de2a-afdf-5cff7b320000</xsl:when>
      <xsl:when test="starts-with($stripped_text,'Corrected an issue')">UUID-00000187-528f-d534-afa7-7bcf327d0001</xsl:when>
      <xsl:otherwise>None</xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>
