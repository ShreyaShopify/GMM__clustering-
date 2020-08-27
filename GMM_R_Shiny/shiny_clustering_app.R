ui <- fluidPage(
  theme = shinytheme('flatly'),
  title = "Data",
  sidebarLayout(
    sidebarPanel(
      conditionalPanel(
        'input.page == "raw_df"',
        checkboxGroupInput(inputId = "show_variables_raw", "Columns to show:",
                           choices = names(raw_df), selected = names(raw_df))
      ),
      conditionalPanel(
        'input.page == "variable_scale"',
        p("We recognized that GMV and transaction counts are heavily skewed."),
        p("So we treated these two columns by setting the maximum & minimum values 
          at three standard deviations away from the original mean")
      ),
      conditionalPanel(
        'input.page == "df"',
        checkboxGroupInput(inputId = "show_variables_df", "Columns to show:",
                           choices = names(df), selected = names(df))
      ),
      conditionalPanel(
        'input.page == "K-means"',
        selectInput('xcol', 'X Variable', k_means_vars, selected = k_means_vars[1]),
        selectInput('ycol', 'Y Variable', k_means_vars, selected = k_means_vars[2]),
        numericInput('clusters', 'Cluster count', 3, min = 1, max = 6)
        ),
      conditionalPanel(
        'input.page == "Correlation"',
        checkboxGroupInput('corr_labs', 'Columns to choose', choices = names(df),
                     selected = c('date_since_creation', 'Total_shop_gmv',
                                  'Total_shop_transactions', 'MRR.1900.01.', 'MRR.0.00'))
      ),
      conditionalPanel(
        'input.page == "Cluster_hist"',
        p("To understand how different clusters differ in attributes, a summary table was produced")
      ),
      conditionalPanel(
        'input.page == "Cluster_analysis"',
        checkboxGroupInput(inputId = "cluster_ana", "Check Column to Analyze",
                     choices = names(sum_df),
                     selected =names(sum_df)) ,
      # shinythemes::themeSelector()
    )),
    mainPanel(
      tabsetPanel(
        id = 'page',
        tabPanel("raw_df", DT::dataTableOutput(outputId ="raw_df")),
        tabPanel("variable_scale", plotOutput(outputId = 'variable_unscale'), 
                 plotOutput(outputId = 'variable_scale')),
        tabPanel("df", DT::dataTableOutput(outputId = "df")),
        tabPanel("K-means", plotOutput(outputId = 'k_means_plot')),
        tabPanel("Correlation", plotOutput(outputId = 'corr_plot')),
        tabPanel("Cluster_hist", plotOutput(outputId = 'cluster_hist')),
        tabPanel("Cluster_analysis", DT::dataTableOutput(outputId = 'analysis'))
      )
    )
  )
)

server <- function(input, output,session) {
  output$raw_df = DT::renderDataTable({
    DT::datatable(raw_df[, input$show_variables_raw, drop = FALSE])
  })
  
  #treatment
  output$variable_unscale = renderPlot({
    ggplot(raw_df, aes(x=Total_shop_gmv)) + 
      geom_density(alpha=.2, fill="#FF6666") +
      xlim(0, 5*10^3) +
      ggtitle('Total_shop_gmv distribution')
  })
  
  output$variable_scale = renderPlot({
    ggplot(raw_df, aes(x=Total_shop_transactions)) + 
      geom_density(alpha=.2, fill="#FF6666") +
      xlim(0, 1500) +
      ggtitle('Total_shop_transactions distribution')
  })
  
  output$df = DT::renderDataTable({
    DT::datatable(df[,input$show_variables_df, drop = FALSE])
  }) 
  
  #kmeans
  selectedData = reactive({sample_n(df[, c(input$xcol, input$ycol)], (dim(df)[1] * 0.25))})
  clusters = reactive({kmeans(selectedData(), input$clusters)})
  output$k_means_plot = renderPlot({
    palette(c("#E41A1C", "#377EB8", "#4DAF4A", "#984EA3",
              "#FF7F00", "#FFFF33", "#A65628", "#F781BF", "#999999"))
    par(mar = c(5.1, 4.1, 0, 1))
    plot(selectedData(),
         col = clusters()$cluster,
         pch = 20, cex = 3)
    points(clusters()$centers, pch = 4, cex = 4, lwd = 4)
  })
  
  #corr plot
  output$corr_plot = renderPlot({
    cols <- as.character(input$corr_labs)
    corr_data = data.frame(df[, cols])
    corr <- round(cor(corr_data), 1)
    ggcorrplot(corr, type = 'lower', method = 'circle')})
  
  #cluster hist
  output$cluster_hist = renderPlot({
    palette(c("#E41A1C", "#377EB8", "#4DAF4A", "#984EA3",
              "#FF7F00", "#FFFF33", "#A65628", "#F781BF", "#999999"))
      ggplot(data=counts_df, aes(x=labels, y=n, fill=Shop.Commerce.Background, width = 1.5)) +
        geom_bar(stat="identity", position=position_dodge(0.7))
  })
  
  #cluter analysis
  output$analysis = DT::renderDataTable({
    DT::datatable(sum_df[,input$cluster_ana, drop = FALSE])
  }) 
}

shinyApp(ui = ui, server = server)
