<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" indent="yes"/>

  <xsl:template match="/">
    <html>
      <head>
        <title><xsl:value-of select="screenplay/title"/></title>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.5; margin: 2em; }
          h1 { border-bottom: 2px solid black; }
          h2 { margin-top: 2em; }
          .credit, .character { margin-bottom: 0.5em; }
          .dialogue { margin-left: 2em; }
        </style>
      </head>
      <body>
        <!-- Title -->
        <h1><xsl:value-of select="screenplay/title"/></h1>

        <!-- Credits Section -->
        <h2>Credits</h2>
        <div class="credit"><strong>Director:</strong> <xsl:value-of select="screenplay/credits/director"/></div>
        <div class="credit"><strong>Producer:</strong> <xsl:value-of select="screenplay/credits/producer"/></div>
        <div class="credit"><strong>Screenplay:</strong> <xsl:value-of select="screenplay/credits/screenplay"/></div>
        <div class="credit"><strong>Adaptation:</strong> <xsl:value-of select="screenplay/credits/adaptation"/></div>
        <div class="credit"><strong>Director of Photography:</strong> <xsl:value-of select="screenplay/credits/directorOfPhotography"/></div>
        <div class="credit"><strong>Music Composer:</strong> <xsl:value-of select="screenplay/credits/musicComposer"/></div>
        <div class="credit"><strong>Special Effects:</strong> <xsl:value-of select="screenplay/credits/specialEffects"/></div>

        <h3>Set Designers</h3>
        <ul>
          <xsl:for-each select="screenplay/credits/setDesigners/designer">
            <li><xsl:value-of select="."/></li>
          </xsl:for-each>
        </ul>

        <h3>Sound Engineers</h3>
        <ul>
          <xsl:for-each select="screenplay/credits/soundEngineers/engineer">
            <li><xsl:value-of select="."/></li>
          </xsl:for-each>
        </ul>

        <div class="credit"><strong>Title Design:</strong> <xsl:value-of select="screenplay/credits/titleDesign"/></div>
        <div class="credit"><strong>Editor:</strong> <xsl:value-of select="screenplay/credits/editor"/></div>
        <div class="credit"><strong>Assistant Director:</strong> <xsl:value-of select="screenplay/credits/assistantDirector"/></div>
        <div class="credit"><strong>Costumes:</strong> <xsl:value-of select="screenplay/credits/costumes"/></div>

        <!-- Characters Section -->
        <h2>Characters</h2>
        <ul>
          <xsl:for-each select="screenplay/characters/character">
            <li>
              <strong><xsl:value-of select="@name"/></strong>
              <xsl:if test="@referred"> (aka <xsl:value-of select="@referred"/>)</xsl:if>
              — played by <xsl:value-of select="@actor"/>
            </li>
          </xsl:for-each>
        </ul>

        <!-- Release Info -->
        <h2>Release Information</h2>
        <p><strong>Year:</strong> <xsl:value-of select="screenplay/release/date"/></p>
        <p><strong>Running Time:</strong> <xsl:value-of select="screenplay/release/runningTime"/> minutes</p>

        <!-- Scenes -->
        <h2>Scenes</h2>
        <xsl:for-each select="screenplay/scenes/scene">
          <div class="scene">
            <h3><xsl:value-of select="heading"/></h3>
            <xsl:for-each select="description">
              <p><xsl:value-of select="."/></p>
            </xsl:for-each>
            <xsl:for-each select="dialogue">
              <p class="dialogue">
                <strong><xsl:value-of select="character"/>:</strong>
                <xsl:for-each select="line">
                  <br/><xsl:value-of select="."/>
                </xsl:for-each>
              </p>
            </xsl:for-each>
            <xsl:if test="transition">
              <p><em>Transition: <xsl:value-of select="transition"/></em></p>
            </xsl:if>
          </div>
        </xsl:for-each>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
