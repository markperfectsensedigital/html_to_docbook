<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xpath-default-namespace="http://www.w3.org/TR/html4/"
    xmlns="http://docbook.org/ns/docbook" xmlns:xi="http://www.w3.org/2001/XInclude" xmlns:xml="http://www.w3.org/XML/1998/namespace">

    <xsl:output method="xml" indent="true"/>

<xsl:template match="/ | @* | node()">

        <xsl:copy>
              <xsl:apply-templates select="@* | node()" />
        </xsl:copy>
 </xsl:template>


    <xsl:template match="@xml:id">
             <xsl:attribute name="xml:id">
            <xsl:value-of select="concat(.,'-node-',generate-id())"/>
        </xsl:attribute>
    </xsl:template>



</xsl:stylesheet>