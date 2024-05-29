<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>
    
    <xsl:template match="/">
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
                <title>Cooling Systems</title>
            </head>
            <body>
                <h2>Cooling Types:</h2>
                <table border="1">
                    <tr>
                        <th>TypeName</th>
                        <th>Description</th>
                        <th>Manufacturer</th>
                        <th>Image</th>
                    </tr>
                    <xsl:for-each select="Database/CoolingTypes/CoolingType">
                        <tr>
                            <td><xsl:value-of select="TypeName"/></td>
                            <td><xsl:value-of select="Description"/></td>
                            <td><xsl:value-of select="Manufacturer"/></td>
                            <td><img>
                                <xsl:attribute name="src">
                                    <xsl:value-of select="ImageURL"/>
                                </xsl:attribute>
                                <xsl:attribute name="alt">
                                    <xsl:value-of select="TypeName"/>
                                </xsl:attribute>
                            </img></td>
                        </tr>
                    </xsl:for-each>
                </table>

                <h2>Models:</h2>
                <table border="1">
                    <tr>
                        <th>ModelName</th>
                        <th>Description</th>
                        <th>CoolingType</th>
                        <th>ReleaseDate</th>
                    </tr>
                    <xsl:for-each select="Database/Models/Model">
                        <tr>
                            <td><xsl:value-of select="ModelName"/></td>
                            <td><xsl:value-of select="Description"/></td>
                            <td><xsl:value-of select="CoolingType"/></td>
                            <td><xsl:value-of select="ReleaseDate"/></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
    
</xsl:stylesheet>
<!-- описывает представление -->