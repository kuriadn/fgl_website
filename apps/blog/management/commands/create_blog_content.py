"""
Django management command to create starter content for the blog app.
Save this file as: blog/management/commands/create_blog_content.py

Make sure you have the management/commands directories created:
mkdir -p blog/management/commands
touch blog/management/__init__.py
touch blog/management/commands/__init__.py
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from apps.blog.models import BlogCategory, BlogPost, BlogComment, BlogSubscriber
from taggit.models import Tag
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Create starter content for the blog'

    def add_arguments(self, parser):
        parser.add_argument(
            '--with-comments',
            action='store_true',
            help='Create sample comments for posts',
        )
        parser.add_argument(
            '--with-subscribers',
            action='store_true',
            help='Create sample newsletter subscribers',
        )

    def handle(self, *args, **options):
        self.stdout.write('Creating blog starter content...')

        # Create or get admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@geo.fayvad.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: {admin_user.username}')

        # Create team member authors
        authors = []
        author_data = [
            {
                'username': 'david_kuria', 
                'first_name': 'Prof. David', 
                'last_name': 'Kuria', 
                'email': 'd.kuria@geo.fayvad.com',
                'is_staff': True
            },
            {
                'username': 'elizabeth_ndegwa', 
                'first_name': 'Elizabeth', 
                'last_name': 'Ndegwa', 
                'email': 'e.ndegwa@geo.fayvad.com',
                'is_staff': True
            },
            {
                'username': 'nehemiah_nyaundi', 
                'first_name': 'Nehemiah', 
                'last_name': 'Nyaundi', 
                'email': 'n.nyaundi@geo.fayvad.com',
                'is_staff': True
            },
            {
                'username': 'wilfred_gichane', 
                'first_name': 'Wilfred', 
                'last_name': 'Gichane', 
                'email': 'w.gichane@geo.fayvad.com',
                'is_staff': True
            },
        ]

        for author_info in author_data:
            author, created = User.objects.get_or_create(
                username=author_info['username'],
                defaults=author_info
            )
            authors.append(author)
            if created:
                author.set_password('fayvad2025')  # Default password for team members
                author.save()
                self.stdout.write(f'Created team member: {author.get_full_name()}')

        authors.append(admin_user)  # Include admin as an author

        # Create blog categories
        categories_data = [
            {
                'name': 'GIS Technology',
                'description': 'Latest developments in Geographic Information Systems and spatial analysis.',
                'color': '#2E8B57',
                'icon': 'fas fa-map'
            },
            {
                'name': 'Land Surveying',
                'description': 'Professional insights on land surveying techniques and best practices.',
                'color': '#4682B4',
                'icon': 'fas fa-drafting-compass'
            },
            {
                'name': 'Drone Mapping',
                'description': 'Aerial surveying and mapping using UAV technology.',
                'color': '#FF6B35',
                'icon': 'fas fa-drone'
            },
            {
                'name': 'Environmental Intelligence',
                'description': 'Environmental monitoring and analysis using geospatial technology.',
                'color': '#228B22',
                'icon': 'fas fa-leaf'
            },
            {
                'name': 'Government Solutions',
                'description': 'GIS and surveying solutions for government agencies.',
                'color': '#6A5ACD',
                'icon': 'fas fa-landmark'
            },
            {
                'name': 'Industry Insights',
                'description': 'Market trends and industry analysis in geospatial technology.',
                'color': '#DC143C',
                'icon': 'fas fa-chart-line'
            }
        ]

        categories = []
        for cat_data in categories_data:
            category, created = BlogCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create blog posts with realistic content
        posts_data = [
            {
                'title': 'Future of GIS Technology in 2025: Trends & Innovations',
                'category': categories[0],  # GIS Technology
                'content': '''
                <p>Geographic Information Systems (GIS) continue to evolve rapidly, driven by advances in cloud computing, artificial intelligence, and real-time data processing. As we move through 2025, several key trends are shaping the future of geospatial technology.</p>
                
                <h3>Cloud-Native GIS Platforms</h3>
                <p>The shift to cloud-native GIS platforms is accelerating, enabling organizations to access powerful spatial analysis tools without the need for extensive on-premises infrastructure. This democratization of GIS technology is opening new possibilities for smaller organizations and developing regions.</p>
                
                <h3>AI-Powered Spatial Analysis</h3>
                <p>Artificial intelligence and machine learning are revolutionizing how we analyze spatial data. From automated feature extraction in satellite imagery to predictive modeling of urban growth patterns, AI is making GIS more intelligent and efficient.</p>
                
                <h3>Real-Time Data Integration</h3>
                <p>The Internet of Things (IoT) is generating unprecedented amounts of location-based data. Modern GIS platforms are evolving to handle real-time data streams, enabling immediate insights and rapid decision-making in critical applications.</p>
                
                <h3>3D and Immersive Technologies</h3>
                <p>Three-dimensional GIS and virtual reality are transforming how we visualize and interact with spatial data. These technologies are particularly valuable for urban planning, environmental modeling, and public engagement initiatives.</p>
                ''',
                'excerpt': 'Explore the cutting-edge trends shaping GIS technology in 2025, from cloud-native platforms to AI-powered spatial analysis.',
                'tags': ['GIS', 'Technology', 'Innovation', 'Cloud Computing', 'AI'],
                'featured': 'hero',
                'read_time': 8
            },
            {
                'title': 'Precision Land Surveying: Best Practices for Accurate Results',
                'category': categories[1],  # Land Surveying
                'content': '''
                <p>Accurate land surveying is the foundation of successful construction projects, property development, and legal boundary determinations. Modern surveying techniques combine traditional methods with cutting-edge technology to achieve unprecedented precision.</p>
                
                <h3>GNSS Technology in Modern Surveying</h3>
                <p>Global Navigation Satellite Systems (GNSS) have revolutionized land surveying, providing centimeter-level accuracy in real-time. RTK (Real-Time Kinematic) corrections and PPP (Precise Point Positioning) techniques are essential tools for modern surveyors.</p>
                
                <h3>Total Station Integration</h3>
                <p>Today's total stations offer seamless integration with GNSS systems and data collectors, streamlining field operations and reducing measurement errors. Robotic total stations enable single-operator workflows, improving efficiency and cost-effectiveness.</p>
                
                <h3>Quality Control Procedures</h3>
                <p>Implementing rigorous quality control procedures is essential for maintaining survey accuracy. This includes redundant measurements, closure checks, and systematic error analysis to ensure reliable results.</p>
                
                <h3>Legal and Regulatory Compliance</h3>
                <p>Understanding local regulations and standards is crucial for professional surveyors. Compliance with state licensing requirements and professional standards ensures the legal validity of survey results.</p>
                ''',
                'excerpt': 'Learn the essential best practices for achieving precision and accuracy in modern land surveying operations.',
                'tags': ['Land Surveying', 'GNSS', 'Precision', 'Best Practices'],
                'featured': 'grid',
                'read_time': 6
            },
            {
                'title': 'Drone Mapping Revolution: Transforming Aerial Surveying',
                'category': categories[2],  # Drone Mapping
                'content': '''
                <p>Unmanned Aerial Vehicles (UAVs) have transformed the surveying and mapping industry, offering cost-effective solutions for data collection across various applications. From construction monitoring to environmental assessment, drone mapping is becoming indispensable.</p>
                
                <h3>Photogrammetry and LiDAR Integration</h3>
                <p>Modern survey drones can be equipped with high-resolution cameras for photogrammetry or LiDAR sensors for direct 3D point cloud generation. The choice between these technologies depends on project requirements and desired accuracy levels.</p>
                
                <h3>Flight Planning and Automation</h3>
                <p>Sophisticated flight planning software enables automated data collection missions, ensuring consistent overlap, optimal ground sample distance, and efficient coverage patterns. Proper planning is crucial for high-quality results.</p>
                
                <h3>Data Processing Workflows</h3>
                <p>Post-processing drone data requires specialized software and techniques. Structure-from-Motion (SfM) algorithms and point cloud processing tools convert raw imagery into accurate orthomosaics, digital elevation models, and 3D models.</p>
                
                <h3>Regulatory Compliance</h3>
                <p>Operating commercial drones requires compliance with aviation regulations. Understanding airspace restrictions, certification requirements, and safety protocols is essential for professional drone operators.</p>
                ''',
                'excerpt': 'Discover how drone mapping technology is revolutionizing aerial surveying and data collection.',
                'tags': ['Drone Mapping', 'UAV', 'Photogrammetry', 'LiDAR', 'Surveying'],
                'featured': 'grid',
                'read_time': 7
            },
            {
                'title': 'Environmental Monitoring with Geospatial Technology',
                'category': categories[3],  # Environmental Intelligence
                'content': '''
                <p>Environmental monitoring has been transformed by advances in geospatial technology, enabling scientists and policymakers to track environmental changes with unprecedented detail and accuracy.</p>
                
                <h3>Satellite Remote Sensing</h3>
                <p>Earth observation satellites provide continuous monitoring of environmental parameters such as vegetation health, water quality, and atmospheric conditions. Platforms like Landsat, Sentinel, and Planet Labs offer high-resolution imagery for environmental analysis.</p>
                
                <h3>Change Detection Analysis</h3>
                <p>Time-series analysis of satellite imagery enables detection of environmental changes over time. This capability is crucial for monitoring deforestation, urban expansion, coastal erosion, and climate change impacts.</p>
                
                <h3>Air Quality Monitoring</h3>
                <p>Ground-based sensor networks combined with satellite data provide comprehensive air quality monitoring systems. Real-time data feeds enable immediate response to pollution events and long-term trend analysis.</p>
                
                <h3>Biodiversity Conservation</h3>
                <p>GIS technology supports biodiversity conservation efforts through habitat mapping, species distribution modeling, and conservation planning. These tools are essential for protecting endangered species and ecosystems.</p>
                ''',
                'excerpt': 'Learn how geospatial technology is advancing environmental monitoring and conservation efforts.',
                'tags': ['Environmental Monitoring', 'Remote Sensing', 'Conservation', 'Satellites'],
                'featured': 'none',
                'read_time': 5
            },
            {
                'title': 'GIS Solutions for Smart Cities and Government',
                'category': categories[4],  # Government Solutions
                'content': '''
                <p>Government agencies are increasingly relying on GIS technology to improve public services, enhance decision-making, and engage with citizens. Smart city initiatives are driving innovation in municipal GIS applications.</p>
                
                <h3>Urban Planning and Development</h3>
                <p>GIS supports comprehensive urban planning by integrating demographic data, infrastructure information, and zoning regulations. Planners can model development scenarios and assess their potential impacts on the community.</p>
                
                <h3>Emergency Management</h3>
                <p>During emergencies, GIS provides critical situational awareness, enabling rapid response and resource allocation. Real-time mapping of incidents, evacuation routes, and emergency resources saves lives and reduces property damage.</p>
                
                <h3>Public Health Applications</h3>
                <p>Spatial analysis of health data helps identify disease patterns, plan healthcare services, and respond to public health emergencies. The COVID-19 pandemic highlighted the importance of geospatial technology in public health.</p>
                
                <h3>Citizen Engagement</h3>
                <p>Web-based GIS applications enable citizens to access government services, report issues, and participate in planning processes. These tools improve transparency and strengthen democracy.</p>
                ''',
                'excerpt': 'Explore how government agencies are leveraging GIS technology for smarter, more efficient public services.',
                'tags': ['Government', 'Smart Cities', 'Urban Planning', 'Emergency Management'],
                'featured': 'sidebar',
                'read_time': 6
            },
            {
                'title': 'The Rise of Digital Twins in Infrastructure Management',
                'category': categories[0],  # GIS Technology
                'content': '''
                <p>Digital twins are revolutionizing infrastructure management by creating dynamic, real-time digital replicas of physical assets. This technology combines GIS, IoT sensors, and 3D modeling to optimize infrastructure operations.</p>
                
                <h3>What Are Digital Twins?</h3>
                <p>A digital twin is a virtual representation of a physical asset that continuously updates based on real-world data. For infrastructure, this means creating detailed 3D models connected to sensor networks that monitor performance in real-time.</p>
                
                <h3>Infrastructure Applications</h3>
                <p>Digital twins are being deployed for bridges, buildings, water systems, and transportation networks. They enable predictive maintenance, operational optimization, and scenario planning for infrastructure managers.</p>
                
                <h3>Integration with GIS</h3>
                <p>GIS provides the spatial framework for digital twins, enabling analysis of infrastructure within its geographic context. This integration supports network analysis, spatial optimization, and regional planning initiatives.</p>
                ''',
                'excerpt': 'Discover how digital twin technology is transforming infrastructure management and maintenance.',
                'tags': ['Digital Twins', 'Infrastructure', 'IoT', '3D Modeling'],
                'featured': 'none',
                'read_time': 4
            },
            {
                'title': 'Choosing the Right Survey Equipment for Your Project',
                'category': categories[1],  # Land Surveying
                'content': '''
                <p>Selecting appropriate survey equipment is crucial for project success. Understanding the capabilities and limitations of different instruments helps surveyors make informed decisions that balance accuracy, efficiency, and cost.</p>
                
                <h3>GNSS Receivers</h3>
                <p>Modern GNSS receivers offer various accuracy levels and features. High-end receivers provide RTK capabilities and multi-constellation support, while basic units offer sufficient accuracy for many applications at lower cost.</p>
                
                <h3>Total Stations vs. Robotic Stations</h3>
                <p>Traditional total stations require two-person crews, while robotic stations enable single-operator workflows. The choice depends on project requirements, crew availability, and budget considerations.</p>
                
                <h3>Laser Scanning Technology</h3>
                <p>Terrestrial laser scanners capture millions of points rapidly, creating detailed 3D models of surveyed areas. This technology is ideal for complex structures, heritage documentation, and as-built surveys.</p>
                ''',
                'excerpt': 'A comprehensive guide to selecting the right surveying equipment for different project requirements.',
                'tags': ['Survey Equipment', 'GNSS', 'Total Station', 'Laser Scanning'],
                'featured': 'none',
                'read_time': 5
            },
            {
                'title': 'ROI Analysis: When Drone Mapping Makes Business Sense',
                'category': categories[2],  # Drone Mapping
                'content': '''
                <p>Drone mapping offers significant cost advantages over traditional surveying methods in many applications. Understanding the return on investment (ROI) helps organizations make informed decisions about adopting drone technology.</p>
                
                <h3>Cost Comparison Analysis</h3>
                <p>Traditional aerial photography and ground surveys can be expensive and time-consuming. Drones reduce costs by eliminating aircraft rental, reducing crew requirements, and accelerating data collection timelines.</p>
                
                <h3>Time Savings</h3>
                <p>Drone surveys can often be completed in hours rather than days or weeks. This speed advantage is particularly valuable for time-sensitive projects or recurring monitoring applications.</p>
                
                <h3>Safety Benefits</h3>
                <p>Drones eliminate the need for personnel to access dangerous areas, reducing safety risks and associated insurance costs. This benefit is particularly important for infrastructure inspection and hazardous site surveys.</p>
                ''',
                'excerpt': 'Learn how to calculate the return on investment for drone mapping projects and when it makes financial sense.',
                'tags': ['ROI', 'Cost Analysis', 'Drone Economics', 'Business Case'],
                'featured': 'none',
                'read_time': 6
            }
        ]

        # Create posts
        posts = []
        for i, post_data in enumerate(posts_data):
            # Calculate publish date (spread over last 3 months)
            days_ago = random.randint(1, 90)
            published_at = timezone.now() - timedelta(days=days_ago)
            
            post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'slug': slugify(post_data['title']),
                    'author': random.choice(authors),
                    'category': post_data['category'],
                    'content': post_data['content'],
                    'excerpt': post_data['excerpt'],
                    'status': 'published',
                    'featured': post_data['featured'],
                    'read_time': post_data['read_time'],
                    'published_at': published_at,
                    'view_count': random.randint(50, 500),
                    'meta_title': post_data['title'][:60],  # Ensure max 60 chars
                    'meta_description': post_data['excerpt'][:160],  # Ensure max 160 chars
                }
            )
            
            if created:
                # Add tags
                for tag_name in post_data['tags']:
                    post.tags.add(tag_name)
                
                posts.append(post)
                self.stdout.write(f'Created post: {post.title}')

        # Create sample comments if requested
        if options['with_comments']:
            comment_authors = [
                {'name': 'Alex Thompson', 'email': 'alex@example.com'},
                {'name': 'Maria Rodriguez', 'email': 'maria@example.com'},
                {'name': 'David Chen', 'email': 'david@example.com'},
                {'name': 'Emily Wilson', 'email': 'emily@example.com'},
                {'name': 'James Brown', 'email': 'james@example.com'},
            ]
            
            sample_comments = [
                "Great article! This really helped me understand the technology better.",
                "Thanks for sharing these insights. Very informative and well-written.",
                "I've been working with similar technology and your points are spot on.",
                "Excellent overview of the current trends. Looking forward to more content like this.",
                "This is exactly what I was looking for. Thank you for the detailed explanation.",
                "Very useful information. I'll definitely be implementing some of these practices.",
                "Fantastic write-up! The examples really help illustrate the concepts.",
                "Great to see such quality content about our industry. Keep it up!",
            ]
            
            for post in posts:
                # Add 1-3 comments per post
                num_comments = random.randint(1, 3)
                for _ in range(num_comments):
                    author = random.choice(comment_authors)
                    comment_content = random.choice(sample_comments)
                    
                    BlogComment.objects.create(
                        post=post,
                        author_name=author['name'],
                        author_email=author['email'],
                        content=comment_content,
                        is_approved=True,
                        created_at=post.published_at + timedelta(days=random.randint(1, 7))
                    )
                
                self.stdout.write(f'Added comments to: {post.title}')

        # Create sample subscribers if requested
        if options['with_subscribers']:
            sample_subscribers = [
                {'email': 'subscriber1@example.com', 'name': 'John Smith'},
                {'email': 'subscriber2@example.com', 'name': 'Jane Doe'},
                {'email': 'subscriber3@example.com', 'name': 'Bob Johnson'},
                {'email': 'subscriber4@example.com', 'name': 'Alice Williams'},
                {'email': 'subscriber5@example.com', 'name': 'Charlie Davis'},
            ]
            
            for sub_data in sample_subscribers:
                subscriber, created = BlogSubscriber.objects.get_or_create(
                    email=sub_data['email'],
                    defaults={
                        'name': sub_data['name'],
                        'is_active': True,
                        'confirmed_at': timezone.now()
                    }
                )
                if created:
                    self.stdout.write(f'Created subscriber: {subscriber.email}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created starter content:\n'
                f'- {len(categories)} categories\n'
                f'- {len(posts)} blog posts\n'
                f'- {len(authors)} authors\n'
                + ('- Sample comments\n' if options['with_comments'] else '')
                + ('- Sample subscribers\n' if options['with_subscribers'] else '')
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                '\nNext steps:\n'
                '1. Add featured images to posts via Django admin\n'
                '2. Customize post content as needed\n'
                '3. Review and adjust category colors/icons\n'
                '4. Test the blog functionality\n'
            )
        )