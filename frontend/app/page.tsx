'use client'

import { useState } from 'react'
import { Layout, Card, Row, Col, Statistic, Progress, Badge, Timeline, Alert, Button, Tabs, Space, Typography } from 'antd'
import { 
  DashboardOutlined, 
  HeartOutlined, 
  FileProtectOutlined, 
  SafetyOutlined,
  AlertOutlined,
  RiseOutlined,
  FallOutlined,
  CheckCircleOutlined,
  WarningOutlined,
  ThunderboltOutlined
} from '@ant-design/icons'

const { Header, Content, Footer } = Layout
const { Title, Text, Paragraph } = Typography

export default function Home() {
  const [activeTab, setActiveTab] = useState('1')

  const riskData = [
    { category: 'Business Health', score: 65, level: 'medium', color: '#faad14' },
    { category: 'Cyber Security', score: 45, level: 'high', color: '#ff4d4f' },
    { category: 'Financial', score: 55, level: 'medium', color: '#faad14' },
    { category: 'Legal', score: 30, level: 'low', color: '#52c41a' },
    { category: 'Market', score: 50, level: 'medium', color: '#faad14' },
  ]

  const alerts: Array<{ id: number; severity: 'error' | 'warning' | 'success' | 'info'; title: string; desc: string }> = [
    { id: 1, severity: 'error', title: 'Data Breach Detected', desc: 'Email found in recent data breach' },
    { id: 2, severity: 'warning', title: 'Cash Flow Warning', desc: 'Negative cash flow trend detected' },
    { id: 3, severity: 'warning', title: 'Contract Risk', desc: 'Unfair termination clause in supplier contract' },
  ]

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ 
        background: '#fff', 
        padding: '0 50px', 
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <Space size="large">
          <div style={{ 
            background: 'linear-gradient(135deg, #1890ff 0%, #722ed1 100%)',
            padding: '8px 12px',
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <SafetyOutlined style={{ fontSize: '24px', color: '#fff' }} />
            <Title level={3} style={{ margin: 0, color: '#fff' }}>VentureGuard AI</Title>
          </div>
          <Text type="secondary" style={{ fontSize: '14px' }}>Predict, Protect, Prosper</Text>
        </Space>
        <Space>
          <Badge status="processing" text="Overall Risk: Medium" />
          <Button type="primary" icon={<ThunderboltOutlined />}>Quick Scan</Button>
        </Space>
      </Header>

      <Content style={{ padding: '24px 50px' }}>
        <Tabs 
          activeKey={activeTab} 
          onChange={setActiveTab}
          size="large"
          items={[
            {
              key: '1',
              label: <span><DashboardOutlined /> Dashboard</span>,
              children: (
                <div>
                  <Alert
                    message="Welcome to VentureGuard AI"
                    description="Your AI-powered business intelligence guardian. Monitor risks, analyze contracts, and get proactive protection for your business."
                    type="info"
                    showIcon
                    closable
                    style={{ marginBottom: 24 }}
                  />

                  <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
                    <Col xs={24} sm={12} lg={6}>
                      <Card>
                        <Statistic
                          title="Overall Risk Score"
                          value={49}
                          suffix="/ 100"
                          valueStyle={{ color: '#faad14' }}
                          prefix={<WarningOutlined />}
                        />
                      </Card>
                    </Col>
                    <Col xs={24} sm={12} lg={6}>
                      <Card>
                        <Statistic
                          title="Active Alerts"
                          value={3}
                          valueStyle={{ color: '#ff4d4f' }}
                          prefix={<AlertOutlined />}
                        />
                      </Card>
                    </Col>
                    <Col xs={24} sm={12} lg={6}>
                      <Card>
                        <Statistic
                          title="Contracts Analyzed"
                          value={12}
                          valueStyle={{ color: '#1890ff' }}
                          prefix={<FileProtectOutlined />}
                        />
                      </Card>
                    </Col>
                    <Col xs={24} sm={12} lg={6}>
                      <Card>
                        <Statistic
                          title="Business Health"
                          value={65}
                          suffix="/ 100"
                          valueStyle={{ color: '#52c41a' }}
                          prefix={<HeartOutlined />}
                        />
                      </Card>
                    </Col>
                  </Row>

                  <Row gutter={[16, 16]}>
                    <Col xs={24} lg={16}>
                      <Card title="Multi-Dimensional Risk Analysis" extra={<Button type="link">View Details</Button>}>
                        <Space direction="vertical" style={{ width: '100%' }} size="large">
                          {riskData.map((risk) => (
                            <div key={risk.category}>
                              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                                <Text strong>{risk.category}</Text>
                                <Badge 
                                  status={risk.level === 'high' ? 'error' : risk.level === 'medium' ? 'warning' : 'success'} 
                                  text={`${risk.score}/100 - ${risk.level.toUpperCase()}`} 
                                />
                              </div>
                              <Progress 
                                percent={risk.score} 
                                strokeColor={risk.color}
                                showInfo={false}
                              />
                            </div>
                          ))}
                        </Space>
                      </Card>
                    </Col>

                    <Col xs={24} lg={8}>
                      <Card title="Active Alerts" extra={<Badge count={alerts.length} />}>
                        <Space direction="vertical" style={{ width: '100%' }}>
                          {alerts.map((alert) => (
                            <Alert
                              key={alert.id}
                              message={alert.title}
                              description={alert.desc}
                              type={alert.severity}
                              showIcon
                              closable
                            />
                          ))}
                        </Space>
                      </Card>

                      <Card title="Recent Activity" style={{ marginTop: 16 }}>
                        <Timeline
                          items={[
                            {
                              color: 'red',
                              children: 'Data breach detected - 2h ago',
                            },
                            {
                              color: 'orange',
                              children: 'Cash flow risk elevated - 1d ago',
                            },
                            {
                              color: 'blue',
                              children: 'Contract analyzed - 3d ago',
                            },
                            {
                              color: 'green',
                              children: 'Security score improved - 1w ago',
                            },
                          ]}
                        />
                      </Card>
                    </Col>
                  </Row>
                </div>
              ),
            },
            {
              key: '2',
              label: <span><HeartOutlined /> Business Health</span>,
              children: (
                <Card title="Business Health Predictor" extra={<Button type="primary">Analyze Now</Button>}>
                  <Alert
                    message="Predictive Business Health Analysis"
                    description="Upload your business data to get AI-powered risk predictions 30-90 days ahead. Includes cash flow analysis, market risk assessment, and actionable recommendations."
                    type="info"
                    showIcon
                    style={{ marginBottom: 24 }}
                  />
                  <Row gutter={[16, 16]}>
                    <Col span={24}>
                      <Card type="inner" title="Upload Business Data">
                        <Space direction="vertical" style={{ width: '100%' }}>
                          <Text>Upload CSV file with monthly revenue and expenses data</Text>
                          <Button type="dashed" block size="large">
                            Click to Upload CSV
                          </Button>
                          <Text type="secondary">Or use demo data to see how it works</Text>
                          <Button type="primary" block>Run Demo Analysis</Button>
                        </Space>
                      </Card>
                    </Col>
                  </Row>
                </Card>
              ),
            },
            {
              key: '3',
              label: <span><FileProtectOutlined /> Contract Analyzer</span>,
              children: (
                <Card title="Smart Contract Analyzer" extra={<Button type="primary">Analyze Contract</Button>}>
                  <Alert
                    message="AI-Powered Contract Analysis"
                    description="Upload contracts to get GPT-4 powered analysis. Detects unfair terms, legal risks, missing clauses, and provides recommendations."
                    type="info"
                    showIcon
                    style={{ marginBottom: 24 }}
                  />
                  <Row gutter={[16, 16]}>
                    <Col span={24}>
                      <Card type="inner" title="Upload Contract">
                        <Space direction="vertical" style={{ width: '100%' }}>
                          <Text>Upload PDF or paste contract text</Text>
                          <Button type="dashed" block size="large">
                            Upload PDF Contract
                          </Button>
                          <Text type="secondary">Or try with demo contract</Text>
                          <Button type="primary" block>Analyze Demo Contract</Button>
                        </Space>
                      </Card>
                    </Col>
                  </Row>
                </Card>
              ),
            },
            {
              key: '4',
              label: <span><SafetyOutlined /> Cyber Security</span>,
              children: (
                <Card title="Cyber Threat Monitor" extra={<Button type="primary">Scan Now</Button>}>
                  <Alert
                    message="Cyber Security Scanning"
                    description="Monitor for data breaches, domain security issues, and cyber threats. Get real-time security scores and recommendations."
                    type="info"
                    showIcon
                    style={{ marginBottom: 24 }}
                  />
                  <Row gutter={[16, 16]}>
                    <Col span={24}>
                      <Card type="inner" title="Security Scan">
                        <Space direction="vertical" style={{ width: '100%' }}>
                          <Text>Enter email or domain to scan</Text>
                          <Space.Compact style={{ width: '100%' }}>
                            <input 
                              placeholder="email@example.com or domain.com" 
                              style={{ 
                                flex: 1, 
                                padding: '8px 12px', 
                                border: '1px solid #d9d9d9',
                                borderRadius: '6px 0 0 6px'
                              }}
                            />
                            <Button type="primary">Scan</Button>
                          </Space.Compact>
                          <Text type="secondary">Or run demo scan</Text>
                          <Button type="primary" block>Run Demo Scan</Button>
                        </Space>
                      </Card>
                    </Col>
                  </Row>
                </Card>
              ),
            },
            {
              key: '5',
              label: <span><AlertOutlined /> Crisis Response</span>,
              children: (
                <Card title="Crisis Response Generator" extra={<Button type="primary">Generate Playbook</Button>}>
                  <Alert
                    message="AI-Powered Crisis Management"
                    description="Get step-by-step crisis response playbooks generated by AI. Covers cash flow crises, data breaches, customer churn, and more."
                    type="info"
                    showIcon
                    style={{ marginBottom: 24 }}
                  />
                  <Row gutter={[16, 16]}>
                    <Col span={24}>
                      <Card type="inner" title="Generate Crisis Playbook">
                        <Space direction="vertical" style={{ width: '100%' }}>
                          <Text>Select crisis type:</Text>
                          <select style={{ 
                            width: '100%', 
                            padding: '8px 12px', 
                            border: '1px solid #d9d9d9',
                            borderRadius: '6px'
                          }}>
                            <option>Cash Flow Crisis</option>
                            <option>Data Breach</option>
                            <option>Customer Churn</option>
                            <option>Legal Issue</option>
                            <option>Reputation Crisis</option>
                            <option>Market Disruption</option>
                          </select>
                          <Button type="primary" block size="large">Generate Playbook</Button>
                          <Text type="secondary">Or view demo playbook</Text>
                          <Button block>View Demo Playbook</Button>
                        </Space>
                      </Card>
                    </Col>
                  </Row>
                </Card>
              ),
            },
          ]}
        />
      </Content>

      <Footer style={{ textAlign: 'center', background: '#f0f2f5' }}>
        <Space split="|">
          <Text>© 2025 VentureGuard AI - GEF2025 Hackathon</Text>
          <Text type="secondary">Powered by AI + Blockchain</Text>
          <Button type="link" size="small">Documentation</Button>
          <Button type="link" size="small">GitHub</Button>
        </Space>
      </Footer>
    </Layout>
  )
}
