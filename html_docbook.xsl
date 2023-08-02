<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:docbook="http://docbook.org/ns/docbook" exclude-result-prefixes="docbook">

    <xsl:output method="xml" indent="true"/>
    <xsl:template match="/">
        <book>
            <title>
                <xsl:value-of select="normalize-space(descendant::h1[@class='CreativeWorkPage-headline'])"/>
            </title>
            <xsl:apply-templates select="descendant::div[@class='StepModule-body RichTextBody']"/>
        </book>
    </xsl:template>

    <xsl:template match="div">
        <xsl:apply-templates select="p"/>
    </xsl:template>

    <xsl:template match="p">
        <para>
            <xsl:apply-templates/>
        </para>
    </xsl:template>

    <xsl:template match="b">
        <emphasis role="bold">
            <xsl:apply-templates/>
        </emphasis>
    </xsl:template>

</xsl:stylesheet>