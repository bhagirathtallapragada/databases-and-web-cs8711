<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:attribute-set name="textbox-attributes">
  <xsl:attribute name="type"> <xsl:value-of select="@datatype"/> </xsl:attribute>
  <xsl:attribute name="name"> <xsl:value-of select="name"/> </xsl:attribute>
  <xsl:attribute name="size"> <xsl:value-of select="size"/> </xsl:attribute>
  <xsl:attribute name="maxlength"> <xsl:value-of select="maxlength"/> </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="checkbox-attributes">
  <xsl:attribute name="type">checkbox</xsl:attribute>
  <xsl:attribute name="id"><xsl:value-of select="caption"/></xsl:attribute>
  <xsl:attribute name="name"><xsl:copy-of select="$checkbox1"/></xsl:attribute>
  <xsl:attribute name="value"><xsl:value-of select="value"/></xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="radio-attributes">
  <xsl:attribute name="type">radio</xsl:attribute>
  <xsl:attribute name="name"><xsl:copy-of select="$radio1"/></xsl:attribute>
  <xsl:attribute name="value"><xsl:value-of select="value"/></xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="submit-attributes">
  <xsl:attribute name="type">submit</xsl:attribute>
  <xsl:attribute name="value"><xsl:value-of select="caption"/></xsl:attribute>
</xsl:attribute-set>

<xsl:template match="/">
  <html>
  <body>
    <form>
    <xsl:apply-templates />
    </form>
  </body>
  </html>
</xsl:template>

<xsl:template match="dataInputForm/title">
    <h1><xsl:value-of select="caption"/></h1>
    <br/>
</xsl:template>

<xsl:template match="break">
    <br />
</xsl:template>

<xsl:template match="textbox">
    <label><xsl:value-of select="name" /></label>
    <input xsl:use-attribute-sets="textbox-attributes" />
</xsl:template>

<xsl:template match="checkboxes">
<label><xsl:value-of  select="caption"/></label>
    <xsl:variable name="checkbox1"><xsl:value-of select="name" /></xsl:variable>
    <xsl:for-each select="checkboxgroup/checkbox">
    <label><xsl:value-of select="caption" /></label>
    <input xsl:use-attribute-sets="checkbox-attributes" >
    <xsl:choose>
    <xsl:when test="@status = 'checked'">
      <xsl:attribute name="checked">true</xsl:attribute>
    </xsl:when>
  </xsl:choose>
  </input>
  </xsl:for-each>
</xsl:template>

<xsl:template match="select">
  <label><xsl:value-of  select="caption"/></label>
  <xsl:variable name="select1"><xsl:value-of select="name" /></xsl:variable>
  <select>
    <xsl:attribute name="name">
        <xsl:value-of select="select/name"/>
    </xsl:attribute>
    <xsl:for-each select="options/option">
      <option>
        <xsl:attribute name="value">
          <xsl:copy-of select="$select1" />
        </xsl:attribute>
        <xsl:value-of select="caption" />
      </option>
    </xsl:for-each>
  </select>
</xsl:template>

<xsl:template match="multiselect">
  <label><xsl:value-of  select="caption"/></label>
  <xsl:variable name="multiselect1"><xsl:value-of select="name" /></xsl:variable>
  <select multiple="true">
    <xsl:attribute name="name">
        <xsl:value-of select="select/name"/>
    </xsl:attribute>
    <xsl:for-each select="options/option">
      <option>
        <xsl:attribute name="value">
          <xsl:copy-of select="$multiselect1" />
        </xsl:attribute>
        <xsl:value-of select="caption" />
      </option>
    </xsl:for-each>
  </select>
</xsl:template>

<xsl:template match="radio">
  <label><xsl:value-of  select="caption"/></label>
  <xsl:variable name="radio1"><xsl:value-of select="name" /></xsl:variable>
  <xsl:for-each select="radiogroup/radioelement">
    <label><xsl:value-of select="caption" /></label>
    <input xsl:use-attribute-sets="radio-attributes" />
  </xsl:for-each>
</xsl:template>

<xsl:template match="submit">
  <input xsl:use-attribute-sets="submit-attributes" />
</xsl:template>
</xsl:stylesheet>