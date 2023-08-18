<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xpath-default-namespace="http://www.w3.org/TR/html4/"
    xmlns="http://docbook.org/ns/docbook">

    <xsl:output method="xml" indent="true"/>
    <xsl:include href="snippets.xsl"/>
    <xsl:template match="/">
        <xsl:apply-templates />
    </xsl:template>

    <xsl:template match="main">
        <section xmlns="http://docbook.org/ns/docbook">
            <xsl:attribute name="xml:id">
                <xsl:value-of select="concat('UUID-',./@id)"/>
            </xsl:attribute>
            <title>
                <xsl:value-of select="normalize-space(h1)"/>
            </title>
            <xsl:apply-templates select="descendant::div[@class='StepModule-body RichTextBody']"/>
        </section>
    </xsl:template>

    <xsl:template match="div[@class='StepModule-body RichTextBody']">
        <xsl:apply-templates/>
    </xsl:template>


    <xsl:template match="div[@class='Enhancement']">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="div[@class='Enhancement-item']">
        <xsl:apply-templates/>
    </xsl:template>

    <!-- Admonitions -->
    <xsl:template match="div[@class='CalloutModule' and @data-content-type='note']">
        <note>
            <xsl:apply-templates select="child::div[@class='CalloutModule-body RichTextBody']"/>
        </note>
    </xsl:template>

    <xsl:template match="div[@class='CalloutModule-body RichTextBody']">
        <para>
            <xsl:apply-templates/>
        </para>
    </xsl:template>

    <!-- Unordered lists -->
    <xsl:template match="ul">
        <itemizedlist>
            <xsl:apply-templates/>
        </itemizedlist>
    </xsl:template>

    <!-- Unordered lists -->
    <xsl:template match="ol">
        <orderedlist>
            <xsl:apply-templates/>
        </orderedlist>
    </xsl:template>


    <xsl:template match="li">
        <listitem>
            <xsl:choose>
                <xsl:when test="not(child::p)">
                    <!-- Some HTML <li> tags have no child <p>, so supply those. -->
                    <para>
                        <xsl:apply-templates/>
                    </para>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates/>
                </xsl:otherwise>

            </xsl:choose>

        </listitem>

    </xsl:template>

    <!-- Figures -->

    <xsl:template match="figure">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="picture">
        <xsl:choose>
            <xsl:when test="following-sibling::figcaption">
                <xsl:apply-templates select="img" mode="formal"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="img" mode="informal"/>
            </xsl:otherwise>
            </xsl:choose>
    </xsl:template>


    <xsl:template match="img" mode="formal">
        <figure>
            <title>
                <xsl:value-of select="../../figcaption/div/div"/>
            </title>
            <mediaobject>
                <imageobject>
                    <imagedata>
                    <xsl:attribute name="fileref">image/uuid-d94b1d9b-42f6-c45a-3bd5-b348d7b6841f-en.png</xsl:attribute>
                    </imagedata>
                </imageobject>
            </mediaobject>
        </figure>
    </xsl:template>

    <xsl:template match="figcaption"/>


    <xsl:template match="img" mode="informal">
        <informalfigure>
            <mediaobject>
                <imageobject>
                    <imagedata>
                    <xsl:attribute name="fileref">image/uuid-d94b1d9b-42f6-c45a-3bd5-b348d7b6841f-en.png</xsl:attribute>
                    </imagedata>
                </imageobject>
            </mediaobject>
        </informalfigure>
    </xsl:template>



    <!-- Paragraph and text -->
    <xsl:template match="p">
        <xsl:choose>
            <xsl:when test="not(text())">
                <!-- Do not process empty paragraphs -->
            </xsl:when>
            <xsl:otherwise>
                <para>
                    <xsl:apply-templates/>
                </para>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>



    <!-- <para>Clicking <emphasis role="bold">Restore</emphasis>, the item enters the <xref xlink:href="#UUID-da503e88-6d8f-e109-eea0-a634f7801df4" remap="UUID-be6907ad-9a53-2b82-e425-d08ea374e17a"/> state.</para>

<para xml:id="UUID-3406ca2a-653e-175e-6a0e-eb9c46c9b443_para-idm13267089487460">Every time an editor posts to an asset's conversation,
Brightspot checks if other editors are mentioned in the post. If so, Brightspot
adds a corresponding message to the conversation topic.</para>  
 -->

    <xsl:template match="span[@class='Term']">
        <!--     <xsl:message><xsl:value-of select="."/></xsl:message> -->
        <phrase>
           <!--  <xsl:attribute name="xml:id">
                <xsl:call-template name="get_snippet_id">
                    <xsl:with-param name="text" select="."/>
                </xsl:call-template>
            </xsl:attribute> -->
            <xsl:apply-templates/>
        </phrase>
    </xsl:template>

    <xsl:template match="b">
        <emphasis role="bold">
            <xsl:apply-templates/>
        </emphasis>
    </xsl:template>

    <xsl:template match="code">
        <code>
            <xsl:apply-templates/>
        </code>
    </xsl:template>



</xsl:stylesheet>