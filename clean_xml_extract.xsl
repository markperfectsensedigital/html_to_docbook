<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xpath-default-namespace="http://www.w3.org/TR/html4/"  xmlns="http://docbook.org/ns/docbook">

    <xsl:output method="xml" indent="true"/>
    <xsl:template match="/">
       
        <xsl:apply-templates />
    
    </xsl:template>

  <xsl:template match="main">
        <section xmlns="http://docbook.org/ns/docbook">
        <title><xsl:value-of select="normalize-space(h1)"/></title>
            <!-- <xsl:apply-templates select="descendant::div[@class='StepModule-body RichTextBody']"/> -->
        </section>
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