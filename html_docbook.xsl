<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xpath-default-namespace="http://www.w3.org/TR/html4/"  xmlns="http://docbook.org/ns/docbook">

    <xsl:output method="xml" indent="true"/>
    <xsl:template match="/">
        <book xmlns="http://docbook.org/ns/docbook">
            <title>Brightspot Documentation</title>
        <chapter>
        <title>Editorial Documentation</title>
            <xsl:apply-templates select="descendant::div[@class='StepModule-body RichTextBody']"/>
    </chapter>
        </book>
    </xsl:template>

    <xsl:template match="div">
    <section>
        <title>
                <xsl:value-of select="normalize-space(descendant::h1[@class='CreativeWorkPage-headline'])"/>
            </title>
        <xsl:apply-templates select="p"/>
        </section>
    </xsl:template>

    <xsl:template match="p">
        <para >
            <xsl:apply-templates/>
        </para>
    </xsl:template>

    <xsl:template match="b">
        <emphasis role="bold" >
            <xsl:apply-templates/>
        </emphasis>
    </xsl:template>

</xsl:stylesheet>