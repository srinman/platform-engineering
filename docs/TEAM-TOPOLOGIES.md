# Team Topologies for Platform Engineering

## Overview

This document defines how teams interact with the platform, their responsibilities, and collaboration patterns. It's based on the [Team Topologies](https://teamtopologies.com/) model adapted for platform engineering.

## Team Types

### 1. Platform Team

**Role**: Build and maintain the internal developer platform

**Mission**: Provide a reliable, secure, and easy-to-use platform that accelerates application delivery

**Responsibilities**:
- Design and implement golden paths
- Maintain baseline cluster configurations
- Develop and maintain KRO ResourceGroups
- Create and update documentation
- Provide developer support and training
- Monitor platform health and performance
- Manage platform upgrades and lifecycle
- Collect and act on developer feedback

**Skills Required**:
- Kubernetes expertise (CKA/CKAD)
- Infrastructure as Code (Terraform)
- GitOps (ArgoCD, Flux)
- Azure cloud platform
- Security and compliance
- Developer experience design
- Technical writing

**Team Size**: 4-8 people

**Structure**:
```
Platform Team Lead
├── Infrastructure Engineers (2-3)
│   └── AKS, Networking, Storage
├── Platform Engineers (2-3)
│   └── KRO, GitOps, Automation
└── Developer Experience Engineer (1)
    └── Documentation, Training, Support
```

**Interaction Modes**:
- **X-as-a-Service**: Provide self-service platform capabilities
- **Enabling**: Help teams onboard and use the platform
- **Collaboration**: Work with app teams on complex requirements

---

### 2. Application Teams (Stream-Aligned Teams)

**Role**: Build and deliver business applications

**Mission**: Deliver value to customers through applications

**Responsibilities**:
- Develop application code
- Define application requirements (resources, ingress, etc.)
- Use platform golden paths
- Monitor application metrics
- Respond to application incidents
- Provide feedback to platform team

**Platform Interaction**:
- Self-service deployment via golden paths
- Consume platform services
- Minimal operational burden
- Focus on business logic

**What They Don't Do**:
- ❌ Manage Kubernetes clusters
- ❌ Configure networking/ingress controllers
- ❌ Set up monitoring infrastructure
- ❌ Create security policies
- ❌ Provision cloud resources directly

**Example Teams**:
- Team Alpha (Customer API)
- Team Beta (Web Frontend)
- Team Gamma (Mobile Backend)

---

### 3. Security/Compliance Team (Enabling Team)

**Role**: Define security requirements and enable secure practices

**Responsibilities**:
- Define security policies
- Create policy-as-code (OPA/Gatekeeper)
- Review and approve deviations from golden paths
- Security training and guidance
- Incident response support
- Compliance auditing

**Platform Interaction**:
- **Enabling**: Help platform and app teams implement security
- **Collaboration**: Joint design of security controls
- Provide requirements, not implementations

**Deliverables to Platform**:
- Security policy requirements
- Gatekeeper policies
- Azure Policy definitions
- Security scanning configurations
- Compliance checklists

---

### 4. SRE/Operations Team (Optional)

**Role**: Ensure reliability and performance at scale

**Note**: In mature platform organizations, many ops tasks are handled by the platform itself. This team exists for complex, large-scale deployments.

**Responsibilities**:
- Define SLOs/SLIs for critical services
- Capacity planning
- Incident response for platform-wide issues
- Performance optimization
- Disaster recovery planning

**Platform Interaction**:
- **Collaboration**: Work with platform team on reliability features
- Use same golden paths as application teams
- Provide observability requirements

---

## Interaction Modes

### X-as-a-Service (Most Common)

Platform team provides services consumed by app teams:

```
┌──────────────────┐
│  Application     │
│  Team            │
│                  │
│  Consumes        │
│  platform APIs   │
└────────┬─────────┘
         │
         │ Self-Service
         │
         ▼
┌──────────────────┐
│  Platform        │
│  (APIs, DSLs)    │
│                  │
│  Clear SLAs      │
└──────────────────┘
```

**Examples**:
- Deploy application via KRO
- Request tenant namespace
- Provision dedicated cluster

**Success Criteria**:
- >90% of requests self-service
- No tickets required
- Clear documentation
- Fast feedback on errors

---

### Enabling (Onboarding & Training)

Platform team helps app teams learn and adopt the platform:

```
┌──────────────────┐
│  Platform Team   │
│                  │
│  Teaches,        │
│  documents,      │
│  supports        │
└────────┬─────────┘
         │
         │ Temporary
         │ Enablement
         ▼
┌──────────────────┐
│  Application     │
│  Team            │
│                  │
│  Learns &        │
│  becomes self-   │
│  sufficient      │
└──────────────────┘
```

**Examples**:
- Onboarding sessions for new teams
- Office hours for questions
- Documentation and tutorials
- Troubleshooting support

**Success Criteria**:
- Teams become self-sufficient within 2 weeks
- Reduced repeat questions
- High documentation satisfaction scores

---

### Collaboration (Complex Requirements)

Joint work on features requiring deep expertise from both teams:

```
┌──────────────────┐     ┌──────────────────┐
│  Application     │◄───►│  Platform        │
│  Team            │     │  Team            │
│                  │     │                  │
│  Domain          │     │  Platform        │
│  expertise       │     │  expertise       │
└──────────────────┘     └──────────────────┘
```

**Examples**:
- Custom integrations (e.g., specific Azure service)
- Performance optimization for high-traffic apps
- Deviation from golden paths
- New use cases not covered by platform

**Success Criteria**:
- Clear scope and timeline
- Shared understanding
- Knowledge transfer
- Feature becomes self-service over time

---

## Team Responsibilities Matrix

| Responsibility | Platform Team | App Team | Security Team | SRE Team |
|---------------|---------------|----------|---------------|----------|
| **Infrastructure** |
| Provision AKS clusters | ✅ Owns | - | - | 🤝 Consults |
| Configure networking | ✅ Owns | - | 🤝 Reviews | - |
| Manage node pools | ✅ Owns | - | - | 🤝 Consults |
| **Platform Services** |
| Develop KRO definitions | ✅ Owns | 💡 Requests | - | - |
| Maintain GitOps | ✅ Owns | 📚 Uses | - | 📚 Uses |
| Create golden paths | ✅ Owns | 💬 Feedback | 🤝 Reviews | 💬 Feedback |
| Platform documentation | ✅ Owns | 💬 Feedback | - | 💬 Feedback |
| **Applications** |
| Write application code | - | ✅ Owns | - | - |
| Deploy applications | 🎓 Enables | ✅ Owns | - | - |
| Monitor app metrics | 🔧 Platform | ✅ Owns | - | 🤝 Complex cases |
| App incident response | 🔧 Platform issues | ✅ Owns | - | 🤝 Major incidents |
| **Security** |
| Define policies | 🤝 Implement | 📚 Follow | ✅ Owns | - |
| Security scanning | ✅ Automate | 📚 Fix issues | 🎓 Enables | - |
| Secrets management | ✅ Provide tools | ✅ Owns secrets | 🎓 Guides | - |
| **Operations** |
| Platform SLOs | ✅ Owns | - | - | 🤝 Defines |
| Capacity planning | ✅ Owns | 💬 Forecast | - | 🤝 Consults |
| Disaster recovery | ✅ Platform DR | ✅ App DR | - | 🤝 Coordinates |

**Legend**:
- ✅ Owns: Primary responsibility
- 🤝 Collaborates: Joint responsibility
- 🎓 Enables: Helps others do it
- 📚 Uses: Consumes service
- 💬 Feedback: Provides input
- 🔧 Platform: Handles platform aspects
- 💡 Requests: Can request features

---

## Communication Channels

### Slack Channels

| Channel | Purpose | Audience |
|---------|---------|----------|
| `#platform-engineering` | General platform questions, announcements | All engineers |
| `#platform-incidents` | Platform incidents and outages | All teams + on-call |
| `#platform-feature-requests` | Feature requests and ideas | All engineers |
| `#platform-internal` | Platform team coordination | Platform team only |

### Regular Meetings

#### Office Hours
- **Frequency**: Weekly (Tuesday 2-3 PM)
- **Purpose**: Q&A, troubleshooting, demos
- **Format**: Open forum, anyone can join
- **Owner**: Platform team (rotating host)

#### Platform Review
- **Frequency**: Monthly
- **Purpose**: Roadmap, metrics review, major decisions
- **Attendees**: Platform team + app team leads
- **Agenda**:
  - DORA metrics review
  - Feature roadmap
  - Incident retrospectives
  - Feedback from teams

#### Developer Feedback Session
- **Frequency**: Quarterly
- **Purpose**: Deep dive on developer experience
- **Attendees**: Platform team + 2-3 developers from each app team
- **Agenda**:
  - Survey results
  - Pain points discussion
  - Improvement prioritization

---

## Onboarding Process

### For Application Teams

**Week 1: Getting Started**
1. Platform overview presentation (1 hour)
2. Assign learning modules (self-paced)
3. Access granted (GitHub, Azure, Slack)
4. Deploy first test application

**Week 2: Hands-On**
1. Office hours session
2. Deploy production application (with support)
3. Set up monitoring dashboards
4. Review security checklist

**Week 3: Independence**
1. Self-service deployment
2. Join platform feedback session
3. Mark onboarding complete

**Success Metrics**:
- First production deployment < 2 weeks
- Self-sufficient (no platform support) by week 3
- >8/10 onboarding satisfaction

### For Platform Team Members

**Month 1: Foundation**
- AKS and Kubernetes deep dive
- GitOps principles and ArgoCD
- Terraform and IaC
- Security and compliance requirements
- Shadow existing team members

**Month 2: Contribution**
- Take ownership of one component
- Participate in office hours
- Review and update documentation
- Handle support requests

**Month 3: Ownership**
- Lead feature development
- On-call rotation
- Present in platform review

---

## Escalation Paths

### Level 1: Self-Service (Target: <5 minutes)
- Documentation
- Example applications
- FAQ

### Level 2: Community Support (Target: <1 hour)
- Slack `#platform-engineering`
- Office hours
- Peer developers

### Level 3: Platform Team Support (Target: <4 hours)
- Create GitHub issue
- Tag `@platform-team` in Slack
- Assigned to platform engineer

### Level 4: Critical Issues (Target: <15 minutes)
- Platform incident (affects multiple teams)
- Page on-call via PagerDuty
- Incident channel `#platform-incidents`

---

## Success Metrics by Team

### Platform Team KPIs
- Platform uptime: >99.9%
- Mean time to recovery (MTTR): <1 hour
- Self-service success rate: >90%
- Developer satisfaction (NPS): >40
- Time to onboard new team: <2 weeks
- Documentation coverage: >90% of features

### Application Team KPIs
- Deployment frequency: Daily+
- Lead time: <1 hour
- Change failure rate: <15%
- MTTR: <1 hour
- Platform adoption: Using golden paths for >80% of deployments

### Security Team KPIs
- Policy compliance: >95%
- Critical vulnerabilities: 0 in production
- Security incidents: 0
- Mean time to patch: <24 hours

---

## Evolution and Scaling

### As the Organization Grows

**10-50 Developers**:
- 1 platform team (4-5 people)
- Generalists handling all platform aspects

**50-200 Developers**:
- Platform team splits focus:
  - Infrastructure sub-team
  - Developer experience sub-team
- Dedicated DevEx engineer
- Community champions in app teams

**200+ Developers**:
- Multiple specialized platform teams:
  - Compute platform team
  - Data platform team
  - Security platform team
  - Developer experience team
- Platform-of-platforms approach
- Regional platform teams

---

## Anti-Patterns to Avoid

❌ **Don't**:
- Create silos (platform vs. app teams)
- Require tickets for standard operations
- Build features without user feedback
- Ignore developer satisfaction metrics
- Make platform team a bottleneck
- Treat app teams as customers to "service" (they're partners!)

✅ **Do**:
- Foster collaboration and shared goals
- Enable self-service
- Collect continuous feedback
- Measure and share metrics
- Empower teams with autonomy
- Treat platform as a product with internal customers

---

## Resources

- [Team Topologies Book](https://teamtopologies.com/)
- [Developer Experience Guide](./DEVELOPER-EXPERIENCE.md)
- [Golden Paths Documentation](./GOLDEN-PATHS.md)
- [Platform Architecture](./PLATFORM-ARCHITECTURE.md)

## Getting Involved

- **Join**: #platform-engineering on Slack
- **Contribute**: Submit PRs to improve the platform
- **Learn**: Attend office hours
- **Feedback**: Share your experience in surveys
