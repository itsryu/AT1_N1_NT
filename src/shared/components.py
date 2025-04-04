from typing import List, Dict, Tuple, Union, Optional, Callable
from pathlib import Path
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph, 
    Spacer, 
    Table, 
    TableStyle, 
    PageBreak,
    Frame,
    PageTemplate,
    BaseDocTemplate
)
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from shared.style import ColorPalette, Fonts
import tkinter as tk
import math

class Card(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        title: str,
        value: str,
        color: str,
        command: Optional[Callable[[], None]] = None
    ) -> None:
        super().__init__(
            parent,
            bg=ColorPalette.SURFACE,
            highlightbackground=ColorPalette.LIGHT,
            highlightthickness=1
        )
        self.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, ipady=10)
        self._create_title(title)
        self.value_label = self._create_value_label(value, color, command)

    def _create_title(self, title: str) -> None:
        tk.Label(
            self,
            text=title,
            font=Fonts.BODY,
            fg=ColorPalette.TEXT_SECONDARY,
            bg=ColorPalette.SURFACE
        ).pack()

    def _create_value_label(
        self,
        value: str,
        color: str,
        command: Optional[Callable[[], None]]
    ) -> tk.Label:
        label = tk.Label(
            self,
            text=value,
            font=("Arial", 14, "bold"),
            fg=color,
            bg=ColorPalette.SURFACE,
            cursor="hand2" if command else ""
        )
        label.pack()
        if command:
            label.bind("<Button-1>", lambda e: command())
        return label

class NativePieChart:
    COLORS: List[str] = [
        ColorPalette.PRIMARY,
        ColorPalette.SUCCESS,
        ColorPalette.WARNING,
        ColorPalette.DANGER,
        ColorPalette.INFO
    ]
    
    def __init__(self, data: Dict[str, int], title: str = "") -> None:
        self.data = data
        self.title = title
    
    def create_tk_chart(self, parent: tk.Widget, width: int = 400, height: int = 300) -> tk.Canvas:
        canvas = tk.Canvas(parent, bg=ColorPalette.BACKGROUND, width=width, height=height, highlightthickness=0)
        
        if not self.data:
            return canvas
            
        total = sum(self.data.values())
        if total == 0:
            return canvas
            
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) * 0.35
        
        canvas.create_text(
            center_x, 30,
            text=self.title,
            font=Fonts.BODY_BOLD,
            fill=ColorPalette.TEXT_PRIMARY
        )
        
        if len(self.data) == 1:
            label, value = next(iter(self.data.items()))
            color = self.COLORS[0]
            
            canvas.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                fill=color,
                outline=ColorPalette.BACKGROUND,
                width=2
            )
            
            canvas.create_text(
                center_x, center_y,
                text=f"{label}\n100%",
                font=Fonts.SMALL_BOLD,
                fill=ColorPalette.TEXT_PRIMARY,
                justify=tk.CENTER
            )
        else:
            start_angle = 0
            for i, (label, value) in enumerate(self.data.items()):
                extent = 360 * (value / total)
                color = self.COLORS[i % len(self.COLORS)]
                
                canvas.create_arc(
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                    start=start_angle,
                    extent=extent,
                    fill=color,
                    outline=ColorPalette.BACKGROUND,
                    width=2
                )
                
                mid_angle = start_angle + extent / 2
                mid_angle_rad = math.radians(mid_angle)
                text_x = center_x + (radius * 0.6) * math.cos(mid_angle_rad)
                text_y = center_y + (radius * 0.6) * math.sin(mid_angle_rad)
                
                percent = (value / total) * 100
                canvas.create_text(
                    text_x, text_y,
                    text=f"{percent:.1f}%",
                    font=Fonts.SMALL_BOLD,
                    fill=ColorPalette.TEXT_PRIMARY
                )
                
                start_angle += extent
        
        return canvas

class NativeBarChart:
    COLORS: List[str] = [
        ColorPalette.PRIMARY,
        ColorPalette.SUCCESS,
        ColorPalette.WARNING,
        ColorPalette.DANGER,
        ColorPalette.INFO
    ]
    
    def __init__(self, data: Dict[str, int], title: str = "") -> None:
        self.data = data
        self.title = title
    
    def create_tk_chart(self, parent: tk.Widget, width: int = 400, height: int = 300) -> tk.Canvas:
        canvas = tk.Canvas(parent, bg=ColorPalette.BACKGROUND, width=width, height=height, highlightthickness=0)
        
        if not self.data:
            return canvas
            
        max_value = max(self.data.values()) if self.data else 1
        bar_width = width / (len(self.data) * 1.8)
        padding = 60
        
        canvas.create_text(
            width // 2, 20,
            text=self.title,
            font=Fonts.BODY_BOLD,
            fill=ColorPalette.TEXT_PRIMARY
        )
        
        canvas.create_line(padding, height - padding, width - padding, height - padding)
        canvas.create_line(padding, padding, padding, height - padding)
        
        for i, (category, value) in enumerate(self.data.items()):
            x = padding + i * (bar_width * 1.5)
            bar_height = (value / max_value) * (height - 2 * padding)
            
            canvas.create_rectangle(
                x, height - padding - bar_height,
                x + bar_width, height - padding,
                fill=self.COLORS[i % len(self.COLORS)],
                outline=""
            )
            
            canvas.create_text(
                x + bar_width / 2, height - padding + 10,
                text=category[:12] + ("..." if len(category) > 12 else ""),
                angle=0,
                anchor="n",
                font=Fonts.SMALL,
                fill=ColorPalette.TEXT_PRIMARY
            )
            
            canvas.create_text(
                x + bar_width / 2, height - padding - bar_height + 10,
                text=str(value),
                font=Fonts.SMALL_BOLD,
                fill=ColorPalette.BUTTON_TEXT
            )
        
        return canvas

class PDFReport:
    COLORS = [
        ColorPalette.PRIMARY,
        ColorPalette.SUCCESS,
        ColorPalette.WARNING,
        ColorPalette.DANGER,
        ColorPalette.INFO
    ]
    
    def __init__(self, controller: object) -> None:
        self.controller = controller
        self._register_fonts()
        self.styles = self._create_custom_styles()
        self.report_path = self._get_report_path()
    
    def _register_fonts(self) -> None:
        try:
            pdfmetrics.registerFont(TTFont('Roboto', 'Roboto-Regular.ttf'))
            pdfmetrics.registerFont(TTFont('Roboto-Bold', 'Roboto-Bold.ttf'))
            pdfmetrics.registerFont(TTFont('Roboto-Italic', 'Roboto-Italic.ttf'))
            self.font_available = True
        except:
            self.font_available = False
    
    def _create_custom_styles(self) -> dict:
        styles = getSampleStyleSheet()
        
        font_normal = 'Roboto' if self.font_available else 'Helvetica'
        font_bold = 'Roboto-Bold' if self.font_available else 'Helvetica-Bold'
        font_italic = 'Roboto-Italic' if self.font_available else 'Helvetica-Oblique'

        if not hasattr(styles, 'MainTitle'):
            styles.add(ParagraphStyle(
                name='MainTitle',
                fontName=font_bold,
                fontSize=18,
                leading=22,
                alignment=TA_CENTER,
                textColor=ColorPalette.DARK,
                spaceAfter=20
            ))
        
        if not hasattr(styles, 'SectionHeader'):
            styles.add(ParagraphStyle(
                name='SectionHeader',
                fontName=font_bold,
                fontSize=14,
                leading=18,
                textColor=ColorPalette.PRIMARY,
                spaceBefore=20,
                spaceAfter=12
            ))
        
        if not hasattr(styles, 'BodyTextEnhanced'):
            styles.add(ParagraphStyle(
                name='BodyTextEnhanced',
                parent=styles['BodyText'],
                fontName=font_normal,
                textColor=ColorPalette.TEXT_PRIMARY,
                spaceAfter=8
            ))
        
        if not hasattr(styles, 'FooterStyle'):
            styles.add(ParagraphStyle(
                name='FooterStyle',
                fontName=font_italic,
                fontSize=8,
                leading=10,
                textColor=ColorPalette.GRAY,
                alignment=TA_CENTER
            ))
        
        return styles
    
    def _get_report_path(self) -> Path:
        reports_dir = Path(__file__).parent.parent.parent / "data" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        return reports_dir / f'library_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    def _header_footer(self, canvas, doc) -> None:
        canvas.saveState()
        
        canvas.setFont('Roboto-Bold' if self.font_available else 'Helvetica-Bold', 10)
        canvas.setFillColor(ColorPalette.PRIMARY)
        canvas.drawString(2*cm, doc.pagesize[1] - 1.5*cm, "Relatório de Estatísticas da Biblioteca")
        
        canvas.setStrokeColor(ColorPalette.PRIMARY)
        canvas.setLineWidth(0.5)
        canvas.line(2*cm, doc.pagesize[1] - 1.6*cm, doc.pagesize[0] - 2*cm, doc.pagesize[1] - 1.6*cm)
        
        canvas.setFont('Roboto' if self.font_available else 'Helvetica', 8)
        canvas.setFillColor(ColorPalette.GRAY)
        footer_text = f"Página {doc.page} • Biblioteca Digital - Sistema de Gerenciamento de Acervo Literário"
        canvas.drawCentredString(doc.pagesize[0]/2, 1*cm, footer_text)
        
        canvas.restoreState()
    
    def generate(self) -> Path:
        try:
            doc = BaseDocTemplate(
                str(self.report_path),
                pagesize=A4,
                leftMargin=2*cm,
                rightMargin=2*cm,
                topMargin=2.5*cm,
                bottomMargin=2.5*cm
            )
            
            frame = Frame(
                doc.leftMargin, doc.bottomMargin, 
                doc.width, doc.height, 
                leftPadding=0, rightPadding=0, 
                topPadding=0, bottomPadding=0
            )
            
            doc.addPageTemplates([
                PageTemplate(id='AllPages', frames=frame, onPage=self._header_footer)
            ])
            
            elements = self._build_content()
            doc.build(elements)
            
            return self.report_path
        
        except Exception as e:
            raise Exception(f"Erro ao gerar PDF: {str(e)}")
    
    def _build_content(self) -> list:
        return [
            *self._create_cover_page(),
            PageBreak(),
            *self._create_summary_section(),
            PageBreak(),
            *self._create_detailed_analysis(),
        ]
    
    def _create_cover_page(self) -> List[Union[Paragraph, Spacer]]:
        return [
            Spacer(1, 10*cm),
            Paragraph("RELATÓRIO DE ESTATÍSTICAS", self.styles['MainTitle']),
            Spacer(1, 1*cm),
            Paragraph(
                "Análise Completa do Acervo e Empréstimos",
                ParagraphStyle(
                    name='CoverSubtitle',
                    parent=self.styles['BodyTextEnhanced'],
                    fontSize=14,
                    alignment=TA_CENTER,
                    textColor=ColorPalette.TEXT_SECONDARY
                )
            ),
            Spacer(1, 5*cm),
            Paragraph(
                f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                ParagraphStyle(
                    name='CoverFooter',
                    parent=self.styles['BodyTextEnhanced'],
                    fontSize=10,
                    alignment=TA_CENTER,
                    textColor=ColorPalette.GRAY
                )
            )
        ]
    
    def _create_summary_section(self) -> List[Union[Paragraph, Table]]:
        stats = self.controller.get_summary_stats()
        
        return [
            Paragraph("RESUMO EXECUTIVO", self.styles['SectionHeader']),
            Paragraph(
                "Principais métricas e indicadores da biblioteca:",
                self.styles['BodyTextEnhanced']
            ),
            Spacer(1, 1*cm),
            self._create_metrics_table(stats),
            Spacer(1, 1*cm),
            Paragraph(
                "Este relatório foi gerado automaticamente pelo sistema de gestão da biblioteca.",
                ParagraphStyle(
                    name='Disclaimer',
                    parent=self.styles['BodyTextEnhanced'],
                    fontSize=9,
                    textColor=ColorPalette.GRAY
                )
            )
        ]
    
    def _create_metrics_table(self, stats: dict) -> Table:
        data = [
            ["📚", "Total de Livros", str(stats.get("total_books", 0))],
            ["👥", "Total de Usuários", str(stats.get("total_users", 0))],
            ["🔄", "Empréstimos Ativos", str(stats.get("active_loans", 0))],
            ["✅", "Empréstimos Finalizados", str(stats.get("completed_loans", 0))],
            ["📈", "Média por Usuário", f"{stats.get('avg_loans_per_user', 0):.1f}"]
        ]
        
        table = Table(data, colWidths=[1.5*cm, 8*cm, 3*cm])
        
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Roboto' if self.font_available else 'Helvetica'),
            ('FONTSIZE', (0, 0), (0, -1), 14),
            ('FONTSIZE', (1, 0), (2, -1), 10),
            ('FONTNAME', (2, 0), (2, -1), 'Roboto-Bold' if self.font_available else 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (-1, -1), ColorPalette.DARK),
            ('BACKGROUND', (0, 0), (-1, 0), ColorPalette.LIGHT),
            ('BOX', (0, 0), (-1, -1), 0.5, ColorPalette.GRAY),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, ColorPalette.GRAY),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [ColorPalette.SURFACE, ColorPalette.LIGHT]),
        ]))
        
        return table
    
    def _create_detailed_analysis(self) -> List[Union[Paragraph, Table, Drawing]]:
        elements = []
        
        elements.extend(self._create_category_section())
        elements.append(PageBreak())
        
        elements.extend(self._create_user_type_section())
        elements.append(PageBreak())
        
        elements.extend(self._create_top_books_section())
        
        return elements
    
    def _create_category_section(self) -> List[Union[Paragraph, Table, Drawing]]:
        section = [
            Paragraph("1. ANÁLISE POR CATEGORIA", self.styles['SectionHeader']),
            Paragraph(
                "Distribuição do acervo por categorias de livros:",
                self.styles['BodyTextEnhanced']
            ),
            Spacer(1, 1*cm)
        ]
        
        bar_data = self.controller.books_by_category()
        if bar_data:
            section.extend([
                self._create_chart_title("Livros por Categoria"),
                self._create_professional_bar_chart(bar_data, "Quantidade"),
                Spacer(1, 0.5*cm),
                self._create_category_table(bar_data)
            ])
        
        return section
    
    def _create_user_type_section(self) -> List[Union[Paragraph, Table, Drawing]]:
        section = [
            Paragraph("2. ANÁLISE POR TIPO DE USUÁRIO", self.styles['SectionHeader']),
            Paragraph(
                "Distribuição de empréstimos por tipo de usuário:",
                self.styles['BodyTextEnhanced']
            ),
            Spacer(1, 1*cm)
        ]
        
        pie_data = self.controller.loans_by_user_type()
        if pie_data:
            section.extend([
                self._create_chart_title("Empréstimos por Tipo de Usuário"),
                self._create_professional_pie_chart(pie_data),
                Spacer(1, 0.5*cm),
                self._create_user_type_table(pie_data)
            ])
        
        return section
    
    def _create_top_books_section(self) -> List[Union[Paragraph, Table]]:
        section = [
            Paragraph("3. LIVROS MAIS EMPRESTADOS", self.styles['SectionHeader']),
            Paragraph(
                "Ranking dos 10 livros mais populares:",
                self.styles['BodyTextEnhanced']
            ),
            Spacer(1, 1*cm)
        ]
        
        top_books = self.controller.most_loaned_books(limit=10)
        if top_books:
            section.append(self._create_top_books_table(top_books))
        
        return section
    
    def _create_chart_title(self, title: str) -> Paragraph:
        return Paragraph(
            title,
            ParagraphStyle(
                name='ChartTitle',
                parent=self.styles['BodyTextEnhanced'],
                fontName='Roboto-Bold' if self.font_available else 'Helvetica-Bold',
                fontSize=11,
                textColor=ColorPalette.DARK,
                spaceAfter=6
            )
        )
    
    def _create_category_table(self, data: Dict[str, int]) -> Table:
        table_data = [["Categoria", "Quantidade", "Percentual"]]
        total = sum(data.values())
        
        for category, count in sorted(data.items(), key=lambda x: x[1], reverse=True):
            percent = (count / total) * 100
            table_data.append([category, str(count), f"{percent:.1f}%"])
        
        return self._create_data_table(table_data, [6*cm, 3*cm, 3*cm])
    
    def _create_user_type_table(self, data: Dict[str, int]) -> Table:
        table_data = [["Tipo de Usuário", "Empréstimos", "Percentual"]]
        total = sum(data.values())
        
        for user_type, count in sorted(data.items(), key=lambda x: x[1], reverse=True):
            percent = (count / total) * 100
            table_data.append([user_type, str(count), f"{percent:.1f}%"])
        
        return self._create_data_table(table_data, [6*cm, 3*cm, 3*cm])
    
    def _create_top_books_table(self, data: list) -> Table:
        table_data = [["#", "Título", "ISBN", "Empréstimos"]]
        
        for idx, (title, isbn, count, _) in enumerate(data, 1):
            table_data.append([str(idx), title, isbn, str(count)])
        
        return self._create_data_table(table_data, [1.5*cm, 8*cm, 3*cm, 2*cm])
    
    def _create_data_table(self, data: list, col_widths: list) -> Table:
        table = Table(data, colWidths=col_widths)
        
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Roboto' if self.font_available else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (-1, 0), 'Roboto-Bold' if self.font_available else 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), ColorPalette.PRIMARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), ColorPalette.BUTTON_TEXT),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, ColorPalette.GRAY),
            ('ROWBACKGROUNDS', (1, 1), (-1, -1), [ColorPalette.SURFACE, ColorPalette.LIGHT]),
        ]))
        
        return table
    
    def _create_professional_bar_chart(self, data: Dict[str, int], y_title: str) -> Drawing:
        drawing = Drawing(15*cm, 10*cm)
        
        bc = VerticalBarChart()
        bc.x = 3*cm
        bc.y = 2*cm
        bc.width = 12*cm
        bc.height = 6*cm
        bc.data = [list(data.values())]
        bc.categoryAxis.categoryNames = list(data.keys())
        bc.valueAxis.valueMin = 0
        bc.barSpacing = 0.15
        bc.barWidth = 0.5
 
        bc.categoryAxis.labels.fontName = 'Roboto' if self.font_available else 'Helvetica'
        bc.categoryAxis.labels.fontSize = 8
        bc.valueAxis.labels.fontName = 'Roboto' if self.font_available else 'Helvetica'
        bc.valueAxis.labels.fontSize = 8

        drawing.add(String(
            1*cm, 5*cm,
            y_title,
            fontName='Roboto-Bold' if self.font_available else 'Helvetica-Bold',
            fontSize=9,
            textAnchor='middle',
            angle=90,
            fillColor=ColorPalette.DARK
        ))
        
        for i, color in enumerate(self.COLORS):
            if i < len(bc.bars):
                r, g, b = self._hex_to_rgb(color)
                bc.bars[i].fillColor = colors.Color(r/255, g/255, b/255)
                bc.bars[i].strokeColor = colors.Color(r*0.8/255, g*0.8/255, b*0.8/255)
                bc.bars[i].strokeWidth = 0.3
        
        drawing.add(bc)
        return drawing
    
    def _create_professional_pie_chart(self, data: Dict[str, int]) -> Drawing:
        drawing = Drawing(15*cm, 10*cm)

        pie = Pie()
        pie.x = 5*cm
        pie.y = 2*cm
        pie.width = 6*cm
        pie.height = 6*cm
        pie.data = list(data.values())
        pie.labels = list(data.keys())
        pie.simpleLabels = 0
        pie.sideLabels = 1
        
        pie.slices.strokeWidth = 0.3
        pie.slices.fontName = 'Roboto' if self.font_available else 'Helvetica'
        pie.slices.fontSize = 8
        
        for i, color in enumerate(self.COLORS):
            if i < len(pie.slices):
                r, g, b = self._hex_to_rgb(color)
                pie.slices[i].fillColor = colors.Color(r/255, g/255, b/255)
                pie.slices[i].strokeColor = colors.black
                pie.slices[i].popout = 5 if len(data) == 1 else 0
        
        legend_x = 12*cm
        legend_y = 6*cm
        
        for i, (label, value) in enumerate(data.items()):
            percent = (value / sum(data.values())) * 100
            drawing.add(Rect(
                legend_x, legend_y - i*0.6*cm, 0.4*cm, 0.4*cm,
                fillColor=pie.slices[i].fillColor,
                strokeColor=colors.black,
                strokeWidth=0.3
            ))
            drawing.add(String(
                legend_x + 0.6*cm, legend_y - i*0.6*cm + 0.2*cm,
                f"{label}: {value} ({percent:.1f}%)",
                fontName='Roboto' if self.font_available else 'Helvetica',
                fontSize=8,
                fillColor=ColorPalette.DARK
            ))
        
        drawing.add(pie)
        return drawing
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        hex_color = hex_color.lstrip('#')
        try:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        except:
            return (0, 0, 0)